import random
import string

from flasgger import swag_from
from flask import Blueprint, request, json, jsonify
from flask_restful import Api, Resource

from config import MSG_SIZE_INIT
from entity.Resp import Resp
from entity.RoomResp import RoomResp
from extensions import db
from models import Room, Timeline, Post, RoomMember, RoomPrototype

bp_room = Blueprint('/room', __name__)
api = Api(bp_room, '/room')


class RoomApi(Resource):
    @swag_from('../swagger/room/retrieve.yaml')
    def get(self, id):
        user_id = request.user.id
        # 获取room ID
        if 'id' in request.args:
            id = request.args['id']
        else:
            return json.jsonify({
                'resultCode': 4000,
                'resultMsg': ''
            })
        # 获取聊天室详情
        if request.method == 'GET':
            # room
            room = Room.query.filter_by(id=id).first()
            if room is None:
                return json.jsonify({
                    'resultCode': 4000,
                    'resultMsg': ''
                })
            # timeline
            timeline_pub = Timeline.query.filter_by(room_id=room.id, timeline_type=0).first()
            timeline_pri = Timeline.query.filter_by(room_id=room.id, timeline_type=1, user_id=user_id).first()
            if timeline_pri is None:
                pass
            # post
            posts_pub = Post.query.filter_by(timeline_id=timeline_pub.id).limit(MSG_SIZE_INIT)
            posts_pri = Post.query.filter_by(timeline_id=timeline_pri.id).limit(MSG_SIZE_INIT)
            # message
            # fixme 多个聊天怎么取数据
            room_resp = RoomResp(
                room=room,
                timeline_pub=timeline_pub,
                timeline_pri=timeline_pri,
                posts_pub=posts_pub,
                posts_pri=posts_pri
            )
            return jsonify(Resp(data=room_resp))

    @swag_from('../swagger/room/create.yaml')
    def post(self):
        data = request.get_json()
        # 批量新建聊天室
        try:
            room_type = int(data['room_type'])
            people_limit = int(data['people_limit'])
            room_count = int(data['room_count'])
        except KeyError:
            return json.dumps(Resp(result_code=4000, result_msg='fail', data=None).__dict__)
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
            tl_pub = Timeline(room_id=room.id, timeline_type=0)
            db.session.add(tl_pub)
            db.session.commit()

            room_count -= 1

        return jsonify(Resp(result_code=2000, result_msg='success', data=None).__dict__)

    @swag_from('../swagger/room/update.yaml')
    def put(self):
        return jsonify(Resp(result_code=2000, result_msg='success', data=None))

    @swag_from('../swagger/room/delete.yaml')
    def delete(self):
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
    @swag_from('../swagger/room/prototype/create.yaml')
    def get(self, id):
        return json.jsonify(Resp(result_code=2000, result_msg='', data=None))

    @swag_from('../swagger/room/prototype/retrieve.yaml')
    def post(self):
        return jsonify(Resp(result_code=2000, result_msg='success', data=None))

    @swag_from('../swagger/room/prototype/update.yaml')
    def put(self):
        return jsonify(Resp(result_code=2000, result_msg='success', data=None))

    @swag_from('../swagger/room/prototype/delete.yaml')
    def delete(self):
        return jsonify(Resp(result_code=2000, result_msg='success', data=None))


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


class RoomMemberApi(Resource):
    @swag_from('../swagger/room/member/create.yaml')
    def get(self, id):
        return json.jsonify(Resp(result_code=2000, result_msg='', data=None).__dict__)

    @swag_from('../swagger/room/member/retrieve.yaml')
    def post(self):
        users = request.get_json()
        if len(users) == 0:
            return jsonify(Resp(result_code=4000, result_msg='no user', data=None).__dict__)
        for user in users:
            try:
                room_id = user['room_id']
                user_id = user['user_id']
                seat_no = user['seat_no']
            except KeyError:
                return jsonify(Resp(result_code=4000, result_msg='key error', data=None).__dict__)

            member = RoomMember(room_id=room_id, user_id=user_id, seat_no=seat_no)
            db.session.add(member)
            db.session.commit()

        return jsonify(Resp(result_code=2000, result_msg='success', data=None).__dict__)

    @swag_from('../swagger/room/member/update.yaml')
    def put(self):
        return jsonify(Resp(result_code=2000, result_msg='success', data=None).__dict__)

    @swag_from('../swagger/room/member/delete.yaml')
    def delete(self):
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
