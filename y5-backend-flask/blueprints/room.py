from flask import Blueprint, request, json
from flask_restful import Api, Resource

from config import MSG_SIZE_INIT
from entity.Resp import Resp
from entity.RoomResp import RoomResp
from models import Room, Timeline, Post

bp_room = Blueprint('/', __name__)
api = Api(bp_room, '/room')


class RoomApi(Resource):
    def get(self, id):
        """
        This is the language awesomeness API
        Call this api passing a language name and get back its features
        ---
        tags:
          - Room
        parameters:
          - name: id
            in: path
            type: string
            required: true
            description: get room by ID
        responses:
          200:
            description: return room with details
            schema:
              id: room id
              properties:
                id:
                  type: string
                  description: room id
                  default: null
                room_name:
                  type: string
                room_desc:
                    type: string
                room_type:
                    type: string
                people_limit:
                    type: string
        """
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
            return json.jsonify(Resp(data=room_resp))


api.add_resource(RoomApi, '/<int:id>')
