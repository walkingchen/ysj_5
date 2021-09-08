import csv
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
from models import Room, Timeline, RoomMember, RoomPrototype, Serializer, User, Redspot, Post
from service import get_friends, query_membership

# error code: 401x


bp_room = Blueprint('/api/room', __name__)
api = Api(bp_room, '/api/room')


class RoomApi(Resource):
    @swag_from('../swagger/room/retrieve.yaml')
    def get(self, id):
        room = Room.query.filter_by(id=id).first()
        if room is None:
            return jsonify(Resp(result_code=4011, result_msg='room not exists', data=None).__dict__)

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

        redspot_list = Redspot.query.filter_by(room_id=room.room_id, user_id=current_user.id).all()
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

        # 检查prototype是否存在
        prototype = RoomPrototype.query.filter_by(id=room_type).first()
        if prototype is None:
            return jsonify(Resp(result_code=4000, result_msg='prototype not exist', data=None).__dict__)

        while room_count > 0:
            room_id = ''.join(random.sample(string.ascii_letters + string.digits, 8))
            room = Room(
                room_id=room_id,
                room_name=room_id,
                room_type=room_type,
                people_limit=people_limit,
                room_desc=room_desc
            )
            db.session.add(room)
            db.session.commit()

            room_count -= 1

        return jsonify(Resp(result_code=2000, result_msg='success', data=None).__dict__)

    @swag_from('../swagger/room/update.yaml')
    def put(self, id):
        data = request.get_json()
        try:
            room_name = data['room_name']
            room_type = data['room_type']
            people_limit = data['people_limit']
        except KeyError:
            return jsonify(Resp(result_code=4000, result_msg='key error', data=None).__dict__)
        if 'room_desc' in data:
            room_desc = data['room_desc']
        else:
            room_desc = None

        room = Room.query.filter_by(id=id).first()
        room.room_name = room_name
        room.room_type = room_type
        room.people_limit = people_limit
        room.room_desc = room_desc

        db.session.add(room)
        db.session.commit()

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
    '/members',
    methods=['POST'],
    endpoint='member/list_create')


@swag_from('../swagger/room/export_room_with_users.yaml')
@bp_room.route('/api/room/export_room_with_users', methods=['GET'])
def export_room_with_users():
    room_members = RoomMember.query.order_by(desc(RoomMember.room_id), RoomMember.seat_no).all()
    with open('static/export_room_with_users.csv', 'w',  encoding='UTF-8') as f:
        csv_writer = csv.writer(f)
        # header = ['id', 'user_id', 'room_type', 'room_id', 'seat_no', 'day', 'topic_no', 'message_id']
        header = ['id', 'room_id', 'seat_no', 'user_id', 'username']
        csv_writer.writerow(header)
        for member in room_members:
            user = User.query.filter_by(id=member.user_id).first()
            line = [str(member.id), str(member.room_id), str(member.seat_no), str(member.user_id), str(user.username)]
            csv_writer.writerow(line)

    return send_from_directory('static', 'export_room_with_users.csv', as_attachment=True)