import random
import string

from flasgger import swag_from
from flask import Blueprint, request, json, jsonify
from flask_login import current_user
from flask_restful import Api, Resource

from entity.Resp import Resp
from entity.RoomResp import RoomResp
from extensions import db
from models import Room, Timeline, Post, RoomMember, RoomPrototype, Serializer, PostComment, PostLike

bp_room = Blueprint('/api/room', __name__)
api = Api(bp_room, '/api/room')


class RoomApi(Resource):
    @swag_from('../swagger/room/retrieve.yaml')
    def get(self, id):
        room = Room.query.filter_by(id=id).first()
        if room is None:
            return json.jsonify({
                'resultCode': 4000,
                'resultMsg': 'room not exists'
            })
        # room members
        members = RoomMember.query.filter_by(room_id=id).all()

        room_resp = RoomResp(
            room=Serializer.serialize(room),
            room_members=Serializer.serialize_list(members)
            # posts_pub=Serializer.serialize_list(posts_pub),
            # posts_pri=Serializer.serialize_list(posts_pri)
        )
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
            return json.dumps(Resp(result_code=4000, result_msg='KeyError', data=None).__dict__)
        except TypeError:
            return json.dumps(Resp(result_code=4000, result_msg='TypeError', data=None).__dict__)

        if 'room_desc' in data:
            room_desc = data['room_desc']
        else:
            room_desc = None

        # 检查prototype是否存在
        prototype = RoomPrototype.query.filter_by(prototype_id=room_type).first()
        if prototype is None:
            return json.dumps(Resp(result_code=4000, result_msg='prototype not exist', data=None).__dict__)

        while room_count > 0:
            room_name = ''.join(random.sample(string.ascii_letters + string.digits, 8))
            room = Room(
                room_name=room_name,
                room_type=room_type,
                people_limit=people_limit,
                room_desc=room_desc
            )
            db.session.add(room)
            db.session.commit()

            # 添加timeline
            timeline_pub = Timeline(room_id=room.id, timeline_type=0)
            db.session.add(timeline_pub)
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
            return json.dumps(Resp(result_code=4000, result_msg='key error', data=None).__dict__)
        if 'room_desc' in data:
            room_desc = data['room_desc']
        else:
            room_desc = None

        room = Room.query.filter_by(id=id).first()
        room(
            room_name=room_name,
            room_type=room_type,
            people_limit=people_limit,
            room_desc=room_desc
        )
        db.session.add(room)
        db.session.commit()

        return jsonify(Resp(result_code=2000, result_msg='success', data=None))

    @swag_from('../swagger/room/delete.yaml')
    def delete(self, id):
        room = Room.query.filter_by(id=id).first()
        if room is None:
            return jsonify(Resp(result_code=4000, result_msg='fail', data=None))

        db.session.delete(room)
        db.session.commit()

        return jsonify(Resp(result_code=2000, result_msg='success', data=None))


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
        return jsonify(Resp(result_code=2000, result_msg='success', data=None).__dict__)

    @swag_from('../swagger/room/prototype/update.yaml')
    def put(self):
        return jsonify(Resp(result_code=2000, result_msg='success', data=None).__dict__)

    @swag_from('../swagger/room/prototype/delete.yaml')
    def delete(self):
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
        users = request.get_json()
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

    # 创建timeline private
    timeline_pri = Timeline(room_id=room_id, user_id=user_id, timeline_type=1)
    db.session.add(timeline_pri)
    db.session.commit()


api.add_resource(
    RoomMemberListApi,
    '/members',
    methods=['POST'],
    endpoint='member/list_create')