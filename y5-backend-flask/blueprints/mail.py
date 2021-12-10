from flasgger import swag_from
from flask import jsonify, request, Blueprint
from flask_login import current_user
from flask_restful import Resource, Api

from entity.Resp import Resp
from extensions import db, scheduler
from models import MailTemplate, Serializer

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
        except TypeError:
            return jsonify(Resp(result_code=4000, result_msg='TypeError', data=None).__dict__)
        except KeyError:
            return jsonify(Resp(result_code=4000, result_msg='KeyError', data=None).__dict__)

        mail = MailTemplate(
            title=title,
            content=content,
            mail_type=mail_type,
            send_hour=send_hour
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
            hour = '*/' + str(send_hour)
            if mail.mail_type == 1:
                scheduler.reschedule_job('job_mail_morning', trigger='cron', hour=hour)
            if mail.mail_type == 2:
                scheduler.reschedule_job('job_mail_night', trigger='cron', hour=hour)

        db.session.commit()

        return jsonify(Resp(
            result_code=2000,
            result_msg='success',
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


class MailListApi(Resource):
    @swag_from('../swagger/mail/list_retrieve.yaml')
    def get(self):
        if not current_user.is_authenticated:
            return jsonify(Resp(result_code=4001, result_msg='need to login', data=None).__dict__)

        mails = MailTemplate.query.all()
        mail_serialized_list = []
        for mail in mails:
            mail_serialized_list.append(Serializer.serialize(mail))

        return jsonify(Resp(result_code=2000, result_msg='success', data=mail_serialized_list).__dict__)


api.add_resource(
    MailListApi,
    '',
    methods=['GET'],
    endpoint='mail/list_retrieve')
