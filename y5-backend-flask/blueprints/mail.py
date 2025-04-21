from apscheduler.triggers.cron import CronTrigger
from flasgger import swag_from
from flask import jsonify, request, Blueprint
from flask_login import current_user
from flask_mail import Message
from flask_restful import Resource, Api

from entity.Resp import Resp
from extensions import db, scheduler, mail
from models import MailTemplate, Serializer, Room, RoomMember, User

bp_mail = Blueprint('/api/mail', __name__)
api = Api(bp_mail, '/api/mail')


class MailApi(Resource):
    @swag_from('../swagger/mail/retrieve.yaml')
    def get(self, id):
        if not current_user.is_authenticated:
            return jsonify(Resp(result_code=4001, result_msg='need to login', data=None).__dict__)

        mail = MailTemplate.query.filter_by(id=id).first()

        return jsonify(Resp(
            result_code=2000,
            result_msg='success',
            data=Serializer.serialize(mail)
        ).__dict__)

    @swag_from('../swagger/mail/create.yaml')
    def post(self):
        if not current_user.is_authenticated:
            return jsonify(Resp(result_code=4001, result_msg='need to login', data=None).__dict__)

        data = request.get_json()
        try:
            title = str(data['title'])
            content = str(data['content'])
            send_hour = int(data['send_hour'])
            mail_type = int(data['mail_type'])
            # 添加room和天次支持
            day = int(data['day'])
            room_id = str(data['room_id'])
        except TypeError:
            return jsonify(Resp(result_code=4000, result_msg='TypeError', data=None).__dict__)
        except KeyError:
            return jsonify(Resp(result_code=4000, result_msg='KeyError', data=None).__dict__)

        mail = MailTemplate(
            title=title,
            content=content,
            mail_type=mail_type,
            send_hour=send_hour,
            room_id=room_id,
            day=day
        )
        db.session.add(mail)
        db.session.commit()

        return jsonify(Resp(
            result_code=2000,
            result_msg='success',
            data=Serializer.serialize(mail)
        ).__dict__)

    @swag_from('../swagger/mail/update.yaml')
    def put(self, id):
        if not current_user.is_authenticated:
            return jsonify(Resp(result_code=4001, result_msg='need to login', data=None).__dict__)

        mail = MailTemplate.query.filter_by(id=id).first()
        if mail is None:
            return jsonify(Resp(
                result_code=4000,
                result_msg='id error',
                data=None
            ).__dict__)

        data = request.get_json()
        if 'title' in data:
            title = str(data['title'])
            mail.title = title

        if 'content' in data:
            content = str(data['content'])
            mail.content = content

        if 'mail_type' in data:
            mail_type = int(data['mail_type'])
            mail.mail_type = mail_type

        if 'send_hour' in data:
            send_hour = int(data['send_hour'])
            mail.send_hour = send_hour

            # reconfigure mail scheduler
            # hour = '*/' + str(send_hour)  # '*/'表示每隔多少时间
            hour = str(send_hour)
            if mail.mail_type == 1:
                scheduler.scheduler.reschedule_job(
                    job_id='job_mail_morning',
                    trigger=CronTrigger(hour=hour)
                )
                # scheduler.modify_job('job_mail_morning', trigger='cron', hour=hour)
            if mail.mail_type == 2:
                scheduler.scheduler.reschedule_job(
                    job_id='job_mail_night',
                    trigger=CronTrigger(hour=hour)
                )
                # scheduler.modify_job('job_mail_night', trigger='cron', hour=hour)

        if 'day' in data:
            day = int(data['day'])
            mail.day = day
        
        if 'room_id' in data:
            room_id = int(data['room_id'])
            mail.room_id = room_id

        db.session.commit()

        return jsonify(Resp(
            result_code=2000,
            result_msg='success',
            data=None
        ).__dict__)

    # @swag_from('../swagger/mail/delete.yaml')
    def delete(self, id):
        if not current_user.is_authenticated:
            return jsonify(Resp(result_code=4001, result_msg='need to login', data=None).__dict__)

        mail = MailTemplate.query.get(id)
        db.session.delete(mail)
        db.session.commit()

        return jsonify(Resp(
            result_code=2000,
            result_msg='Mail template deleted',
            data=None
        ).__dict__)


api.add_resource(
    MailApi,
    '/<int:id>',
    methods=['GET'],
    endpoint='mail/retrieve')
api.add_resource(
    MailApi,
    '',
    methods=['POST'],
    endpoint='mail/create')
api.add_resource(
    MailApi,
    '/<int:id>',
    methods=['PUT'],
    endpoint='mail/update')
api.add_resource(
    MailApi,
    '/<int:id>',
    methods=['DELETE'],
    endpoint='mail/delete')


class MailListApi(Resource):
    @swag_from('../swagger/mail/list_retrieve.yaml')
    def get(self):
        if not current_user.is_authenticated:
            return jsonify(Resp(result_code=4001, result_msg='need to login', data=None).__dict__)

        mails = MailTemplate.query.all()
        mail_serialized_list = []
        for mail in mails:
            room = Room.query.get(mail.room_id)
            if room is None:
                continue
            mail_serialized = Serializer.serialize(mail)
            mail_serialized['room_name'] = room.room_name
            mail_serialized_list.append(mail_serialized)

        return jsonify(Resp(result_code=2000, result_msg='success', data=mail_serialized_list).__dict__)


api.add_resource(
    MailListApi,
    '',
    methods=['GET'],
    endpoint='mail/list_retrieve')


class EmergencyEmailApi(Resource):
    @swag_from('../swagger/mail/emergency_mail.yaml')
    def post(self):
        data = request.get_json()
        title = str(data['title'])
        content = str(data['content'])
        room_id = int(data['room_id'])
        member_id = None
        if 'member_id' in data:
            member_id = data['member_id']

        with mail.connect() as conn:
            subject = title
            if member_id is None:
                members = RoomMember.query.filter_by(room_id=room_id).all()
                for member in members:
                    user = User.query.filter_by(id=member.id).first()
                    msg = Message(recipients=[user.email],
                                  body=content,
                                  subject=subject,
                                  sender=("Chattera Team Team", "chattera.platform@gmail.com"))
            else:
                user = User.query.filter_by(id=member_id).first()
                msg = Message(recipients=[user.email],
                              body=content,
                              subject=subject,
                              sender=("Chattera Team Team", "chattera.platform@gmail.com"))

            conn.send(msg)

        return jsonify(Resp(result_code=2000, result_msg='success', data=None).__dict__)


api.add_resource(
    EmergencyEmailApi,
    '/emergency_mail',
    methods=['POST'],
    endpoint='mail/emergency_email')