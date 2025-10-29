import csv
import datetime
import random
import string

from flasgger import swag_from
from flask import Blueprint, request, json, jsonify, send_from_directory
from flask_login import current_user, login_required
from flask_restful import Api, Resource
from sqlalchemy import desc

from entity.Resp import Resp
from entity.RoomResp import RoomResp
from extensions import db, socketio
from models import Room, Timeline, RoomMember, RoomPrototype, Serializer, User, Redspot, PublicPost, PostComment, \
    PostLike, PostFlag
from service import get_friends, query_membership
from utils.mail_async import send_room_activation_email_async

# error code: 401x


bp_room = Blueprint('/api/room', __name__)
api = Api(bp_room, '/api/room')


class RoomApi(Resource):
    @swag_from('../swagger/room/retrieve.yaml')
    def get(self, id):
        room = Room.query.filter_by(id=id).first()
        if room is None:
            return jsonify(Resp(result_code=4011, result_msg='room not exists', data=None).__dict__)

        if room.activated != 1:
            return jsonify(Resp(result_code=4012, result_msg='room not activated', data=None).__dict__)

        if not current_user.is_authenticated:
            return jsonify(Resp(result_code=4001, result_msg='need to login', data=None).__dict__)

        friends = get_friends(room=room, user_id=current_user.id)

        members = {'me': None, 'friends': []}
        u = query_membership(room_id=id, user_id=current_user.id)
        if u is not None:
            members['me'] = u._asdict()
        for friend in friends:
            m = query_membership(room_id=id, user_id=friend.user_id)
            if m is not None:
                members['friends'].append(m._asdict())

        redspot_list = Redspot.query.filter_by(room_id=room.id, user_id=current_user.id).all()
        redspot_list_serialized = Serializer.serialize_list(redspot_list)

        room_serialized = room.serialize()
        room_resp = RoomResp(
            room=room_serialized,
            members=members,
            redspot_list=redspot_list_serialized
        )

        socketio.emit('friend_online', {'user_id': current_user.id}, room_id=id)

        return jsonify(Resp(result_code=2000, result_msg='success', data=room_resp.__dict__).__dict__)

    @swag_from('../swagger/room/create.yaml')
    def post(self):
        data = request.get_json()
        # 批量新建聊天室
        try:
            room_type = int(data['room_type'])
            people_limit = int(data['people_limit'])
            room_count = int(data['room_count'])
        except KeyError:
            return jsonify(Resp(result_code=4000, result_msg='KeyError', data=None).__dict__)
        except TypeError:
            return jsonify(Resp(result_code=4000, result_msg='TypeError', data=None).__dict__)

        if 'room_desc' in data:
            room_desc = data['room_desc']
        else:
            room_desc = None

        if 'activated' in data:
            activated = data['activated']
        else:
            activated = 0
        if 'publish_time' in data:
            publish_time = data['publish_time']
        else:
            publish_time = 7

        if 'condition' in data:
            condition = data['condition']
        else:
            condition = None

        # 检查prototype是否存在
        prototype = RoomPrototype.query.filter_by(id=room_type).first()
        if prototype is None:
            return jsonify(Resp(result_code=4000, result_msg='prototype not exist', data=None).__dict__)

        while room_count > 0:
            room_id = ''.join(random.sample(string.digits, 6))
            room_name = 'room_' + room_id
            room = Room(
                room_id=room_id,
                room_name=room_name,
                room_type=room_type,
                people_limit=people_limit,
                room_desc=room_desc,
                activated=activated,
                publish_time=publish_time,
                condition=condition
            )
            db.session.add(room)
            db.session.commit()

            room_count -= 1

        return jsonify(Resp(result_code=2000, result_msg='success', data=None).__dict__)

    @swag_from('../swagger/room/update.yaml')
    def put(self, id):
        data = request.get_json()

        room = Room.query.filter_by(id=id).first()
        if 'room_name' in data:
            room_name = data['room_name']
            room.room_name = room_name

        if 'room_type' in data:
            room_type = data['room_type']
            room.room_type = room_type

        if 'people_limit' in data:
            people_limit = data['people_limit']
            room.people_limit = people_limit

        if 'room_desc' in data:
            room_desc = data['room_desc']
            room.room_desc = room_desc

        if 'activated' in data:
            activated = data['activated']
            room.activated = activated

            if activated == 1:
                # 更新room的activated_at字段，设置其value为最新时间
                room.activated_at = datetime.datetime.now()

        if 'publish_time' in data:
            publish_time = data['publish_time']
            room.publish_time = publish_time

        if 'condition' in data:
            condition = data['condition']
            room.condition = condition

        db.session.add(room)
        db.session.commit()

        # 邮件发送移到数据库事务之外，异步执行
        if 'activated' in data and data['activated'] == 1:
            members = RoomMember.query.filter_by(room_id=room.id).all()
            for member in members:
                user = User.query.get(member.user_id)
                if user and user.email is not None:
                    send_activation_email_async(user.email, user.nickname)

        return jsonify(Resp(result_code=2000, result_msg='success', data=None).__dict__)

    @swag_from('../swagger/room/delete.yaml')
    def delete(self, id):
        room = Room.query.filter_by(id=id).first()
        if room is None:
            return jsonify(Resp(result_code=4000, result_msg='fail', data=None).__dict__)

        db.session.delete(room)
        db.session.commit()

        return jsonify(Resp(result_code=2000, result_msg='success', data=None).__dict__)


api.add_resource(
    RoomApi,
    '/<int:id>',
    methods=['GET'],
    endpoint='retrieve')
api.add_resource(
    RoomApi,
    '',
    methods=['POST'],
    endpoint='create')
api.add_resource(
    RoomApi,
    '/<int:id>',
    methods=['PUT'],
    endpoint='update')
api.add_resource(
    RoomApi,
    '/<int:id>',
    methods=['DELETE'],
    endpoint='delete')


class RoomListApi(Resource):
    @swag_from('../swagger/room/list_retrieve.yaml')
    def get(self):
        try:
            if 'room_type' in request.args:
                room_type = int(request.args['room_type'])
                rooms = Room.query.filter_by(room_type=room_type).all()
            else:
                rooms = Room.query.all()
            rooms_serialized = Serializer.serialize_list(rooms)

            return jsonify(Resp(result_code=2000, result_msg='success', data=rooms_serialized).__dict__)
        except TypeError:
            return jsonify(Resp(result_code=4000, result_msg='type error', data=None).__dict__)


api.add_resource(
    RoomListApi,
    '',
    methods=['GET'],
    endpoint='list_retrieve')


class RoomPrototypeApi(Resource):
    @swag_from('../swagger/room/prototype/retrieve.yaml')
    def get(self, id):
        prototype = RoomPrototype.query.filter_by(id=id).first()
        if prototype is None:
            return jsonify(Resp(result_code=2000, result_msg='prototype not found', data=None).__dict__)

        return json.jsonify(Resp(
            result_code=2000,
            result_msg='success',
            data=Serializer.serialize(prototype)
        ).__dict__)

    @swag_from('../swagger/room/prototype/create.yaml')
    def post(self):
        data = request.get_json()
        try:
            prototype_name = data['prototype_name']
            people_limit = int(data['people_limit'])
            friendship = data['friendship']
        except KeyError:
            return jsonify(Resp(result_code=4000, result_msg='KeyError', data=None).__dict__)
        except TypeError:
            return jsonify(Resp(result_code=4000, result_msg='TypeError', data=None).__dict__)

        prototype = RoomPrototype(prototype_name=prototype_name, people_limit=people_limit, friendship=friendship)
        db.session.add(prototype)
        db.session.commit()

        return jsonify(Resp(result_code=2000, result_msg='success', data=None).__dict__)

    @swag_from('../swagger/room/prototype/update.yaml')
    def put(self, id):
        return jsonify(Resp(result_code=2000, result_msg='success', data=None).__dict__)

    @swag_from('../swagger/room/prototype/delete.yaml')
    def delete(self, id):
        prototype = RoomPrototype.query.filter_by(id=id).first()
        if prototype is None:
            return jsonify(Resp(result_code=4000, result_msg='can not find prototype', data=None).__dict__)

        db.session.delete(prototype)
        db.session.commit()

        return jsonify(Resp(result_code=2000, result_msg='success', data=None).__dict__)


api.add_resource(
    RoomPrototypeApi,
    '/prototype/<int:id>',
    methods=['GET'],
    endpoint='prototype/retrieve')
api.add_resource(
    RoomPrototypeApi,
    '/prototype',
    methods=['POST'],
    endpoint='prototype/create')
api.add_resource(
    RoomPrototypeApi,
    '/prototype/<int:id>',
    methods=['PUT'],
    endpoint='prototype/update')
api.add_resource(
    RoomPrototypeApi,
    '/prototype/<int:id>',
    methods=['DELETE'],
    endpoint='prototype/delete')


class RoomPrototypeListApi(Resource):
    @swag_from('../swagger/room/prototype/list_retrieve.yaml')
    def get(self):
        prototypes = RoomPrototype.query.all()
        return json.jsonify(Resp(
            result_code=2000,
            result_msg='success',
            data=Serializer.serialize_list(prototypes)
        ).__dict__)


api.add_resource(
    RoomPrototypeListApi,
    '/prototype',
    methods=['GET'],
    endpoint='prototype/list_retrieve')


class RoomMemberApi(Resource):
    @swag_from('../swagger/room/member/retrieve.yaml')
    def get(self, id):
        return json.jsonify(Resp(result_code=2000, result_msg='', data=None).__dict__)

    @swag_from('../swagger/room/member/create.yaml')
    def post(self):
        user = request.get_json()
        try:
            room_id = user['room_id']
            user_id = user['user_id']
            seat_no = user['seat_no']
        except KeyError:
            return jsonify(Resp(result_code=4000, result_msg='KeyError', data=None).__dict__)
        except TypeError:
            return jsonify(Resp(result_code=4000, result_msg='TypeError', data=None).__dict__)
        create_member(room_id=room_id, user_id=user_id, seat_no=seat_no)

        return jsonify(Resp(result_code=2000, result_msg='success', data=None).__dict__)

    @swag_from('../swagger/room/member/update.yaml')
    def put(self, id):
        return jsonify(Resp(result_code=2000, result_msg='success', data=None).__dict__)

    @swag_from('../swagger/room/member/delete.yaml')
    def delete(self, id):
        member = RoomMember.query.filter_by(id=id).first()
        if member is None:
            return jsonify(Resp(result_code=4000, result_msg='fail', data=None).__dict__)

        db.session.delete(member)
        db.session.commit()

        return jsonify(Resp(result_code=2000, result_msg='success', data=None).__dict__)


api.add_resource(
    RoomMemberApi,
    '/member/<int:id>',
    methods=['GET'],
    endpoint='member/retrieve')
api.add_resource(
    RoomMemberApi,
    '/member',
    methods=['POST'],
    endpoint='member/create')
api.add_resource(
    RoomMemberApi,
    '/member/<int:id>',
    methods=['PUT'],
    endpoint='member/update')
api.add_resource(
    RoomMemberApi,
    '/member/<int:id>',
    methods=['DELETE'],
    endpoint='member/delete')


class RoomMemberListApi(Resource):
    @swag_from('../swagger/room/member/list_retrieve.yaml')
    def get(self, room_id):
        room_members = RoomMember.query.filter_by(room_id=room_id).all()
        if room_members is None:
            return jsonify(Resp(result_code=4000, result_msg='not found', data=None).__dict__)

        room_member_serialized = []
        for member in room_members:
            member_serialized = Serializer.serialize(member)
            user = User.query.filter_by(id=member.user_id).first()
            if user is not None:
                member_serialized['user_info'] = {
                    'nickname': user.nickname,
                    'email': user.email
                }
                room_member_serialized.append(member_serialized)

        return jsonify(Resp(result_code=2000, result_msg='success', data=room_member_serialized).__dict__)

    @swag_from('../swagger/room/member/list_create.yaml')
    def post(self):
        data = request.get_json()
        users = data['users']
        if len(users) == 0:
            return jsonify(Resp(result_code=4000, result_msg='empty params', data=None).__dict__)
        for user in users:
            try:
                room_id = user['room_id']
                user_id = user['user_id']
                seat_no = user['seat_no']
            except KeyError:
                return jsonify(Resp(result_code=4000, result_msg='KeyError', data=None).__dict__)
            except TypeError:
                return jsonify(Resp(result_code=4000, result_msg='TypeError', data=None).__dict__)
            create_member(room_id=room_id, user_id=user_id, seat_no=seat_no)

        return jsonify(Resp(result_code=2000, result_msg='success', data=None).__dict__)


def create_member(room_id, user_id, seat_no):
    member = RoomMember(room_id=room_id, user_id=user_id, seat_no=seat_no)
    db.session.add(member)
    db.session.commit()


api.add_resource(
    RoomMemberListApi,
    '/members/<int:room_id>',
    methods=['GET'],
    endpoint='member/list_retrieve')


api.add_resource(
    RoomMemberListApi,
    '/members',
    methods=['POST'],
    endpoint='member/list_create')


@swag_from('../swagger/room/export_room.yaml')
@bp_room.route('/api/room/export_room', methods=['GET'])
def export_room():
    rooms = Room.query.all()
    with open('static/export_room.csv', 'w',  encoding='UTF-8', newline='') as f:
        csv_writer = csv.writer(f)
        # header = ['id', 'user_id', 'room_type', 'room_id', 'seat_no', 'day', 'topic_no', 'message_id']
        header = ['id', 'room_name', 'room_desc', 'room_type', 'people_limit', 'created_at', 'updated_at']
        csv_writer.writerow(header)
        for room in rooms:
            line = [str(room.id), str(room.room_name), room.room_desc, str(room.people_limit),
                    room.created_at, room.updated_at]
            csv_writer.writerow(line)

    return send_from_directory('static', 'export_room.csv', as_attachment=True)


@swag_from('../swagger/room/room_stats.yaml')
@bp_room.route('/api/room/room_stats', methods=['GET'])
def room_stats():
    data = request.args
    room_id = data['room_id']
    room = Room.query.get(room_id)

    today = datetime.datetime.today().date()
    tomorrow = datetime.datetime.today().date() + datetime.timedelta(days=1)

    day_activated = room.activated_at
    day = today - day_activated.date()
    day = day.days
    # day = 8
    room_members = RoomMember.query.filter_by(room_id=room.id).all()
    member_ids = []
    for member in room_members:
        member_ids.append(member.user_id)

    # room level
    new_post_count = PublicPost.query.filter_by(room_id=room.id).filter_by(topic=day).count()

    # comments
    new_comment_count = PostComment.query.filter(PostComment.user_id.in_(tuple(member_ids))).filter(
        PostComment.created_at >= today,
        PostComment.created_at < tomorrow
    ).count()

    # likes
    new_like_count = PostLike.query.filter(PostLike.user_id.in_(tuple(member_ids))).filter(
        PostLike.created_at >= today,
        PostLike.created_at < tomorrow
    ).count()

    # flags
    new_flag_count = PostFlag.query.filter(PostFlag.user_id.in_(tuple(member_ids))).filter(
        PostFlag.created_at >= today,
        PostFlag.created_at < tomorrow
    ).count()

    return jsonify(Resp(result_code=2000, result_msg='success', data={
        'new_post_count': new_post_count,
        'new_comment_count': new_comment_count,
        'new_like_count': new_like_count,
        'new_flag_count': new_flag_count
    }).__dict__)

