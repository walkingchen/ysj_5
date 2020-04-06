from flasgger import swag_from
from flask import Blueprint, request, json, jsonify
from flask_login import current_user
from flask_restful import Api, Resource
from flask_socketio import emit

from entity.Resp import Resp
from extensions import db
from models import Post, PostComment, PostLike, Serializer, Timeline, User, Room, RoomPrototype, RoomMember
from service import get_friends, process_posts

bp_post = Blueprint('/api/post', __name__)
api = Api(bp_post, '/api/post')

TIMELINE_PUB = 0
TIMELINE_PRI = 1
TIMELINE_ALL = 2
MSG_SIZE_INIT = 50


class PostApi(Resource):
    @swag_from('../swagger/post/retrieve.yaml')
    def get(self, id):
        data = request.get_json()
        timeline_id = data['timeline_id']

        return jsonify(Resp(
            result_code=2000,
            result_msg='success',
            data=None
        ).__dict__)

    @swag_from('../swagger/post/create.yaml')
    def post(self):
        user_id = request.user.id
        data = request.get_json()

        try:
            timeline_type = data['timeline_type']
            post_content = data['post_content']
            post_type = data['post_type']
            keywords = data['keywords']
            room_id = data['room_id']
        except TypeError:
            return json.dumps(Resp(result_code=4000, result_msg='TypeError', data=None).__dict__)
        except KeyError:
            return json.dumps(Resp(result_code=4000, result_msg='KeyError', data=None).__dict__)
        if 'post_title' in data:
            post_title = data['post_title']
        else:
            post_title = None

        post = Post(
            timeline_type=timeline_type,
            post_title=post_title,
            post_content=post_content,
            keywords=keywords,
            post_type=post_type,
            user_id=user_id,
            room_id=room_id
        )
        db.session.add(post)
        db.session.commit()

        # 通知好友刷新timeline
        emit('pull', room=room_id)

        return jsonify(Resp(
            result_code=2000,
            result_msg='success',
            data=Serializer.serialize(post)
        ).__dict__)

    @swag_from('../swagger/post/update.yaml')
    def put(self, id):
        post = Post.query.filter_by(id=id).first()
        post.timeline_type = 2  # 0: public; 1: private; 2: both
        db.session.commit()

        emit('pull', room=post.room_id)  # fixme

        return jsonify(Resp(
            result_code=2000,
            result_msg='success',
            data=None
        ).__dict__)

    @swag_from('../swagger/post/delete.yaml')
    def delete(self, id):
        post = Post.query.filter_by(id=id).first()
        db.session.delete(post)
        db.session.commit()

        return jsonify(Resp(
            result_code=2000,
            result_msg='success',
            data=None
        ).__dict__)


api.add_resource(
    PostApi,
    '/<int:id>',
    methods=['GET'],
    endpoint='post/retrieve')
api.add_resource(
    PostApi,
    '/',
    methods=['POST'],
    endpoint='post/create')
api.add_resource(
    PostApi,
    '/<int:id>',
    methods=['PUT'],
    endpoint='post/update')
api.add_resource(
    PostApi,
    '/<int:id>',
    methods=['DELETE'],
    endpoint='post/delete')


class PostApi(Resource):
    @swag_from('../swagger/post/list_retrieve.yaml')
    def get(self):
        if current_user is None:
            return json.dumps(Resp(result_code=4000, result_msg='need to login', data=None).__dict__)

        data = request.args
        try:
            room_id = data['room_id']
            timeline_type = data['timeline_type']
        except KeyError:
            return json.dumps(Resp(result_code=4000, result_msg='KeyError', data=None).__dict__)
        except TypeError:
            return json.dumps(Resp(result_code=4000, result_msg='TypeError', data=None).__dict__)

        # user_id = current_user.id
        user_id = 18
        if user_id is None:
            return json.dumps(Resp(result_code=4000, result_msg='user id is none', data=None).__dict__)

        room = Room.query.filter_by(id=room_id).first()
        friends = get_friends(room=room, user_id=user_id)

        friend_ids = []
        for friend in friends:
            friend_ids.append(friend.user_id)

        if timeline_type == TIMELINE_ALL:
            timeline_types = [0, 1]
        else:
            timeline_types = [timeline_type]
        posts = Post.query.filter(
            Post.room_id == room_id,
            Post.user_id.in_(friend_ids),
            Post.timeline_type.in_(timeline_types)
        ).limit(MSG_SIZE_INIT).all()
        # 为每篇post添加评论、点赞
        posts_serialized = Serializer.serialize_list(posts)
        process_posts(posts=posts_serialized, user_id=user_id)

        return jsonify(Resp(result_code=2000, result_msg='success', data=posts_serialized).__dict__)


api.add_resource(
    PostApi,
    '/',
    methods=['GET'],
    endpoint='post/list_retrieve')


class CommentApi(Resource):
    @swag_from('../swagger/post/comment/retrieve.yaml')
    def get(self, id):
        comment = PostComment.query.filter_by(id=id).first()
        comment_serialized = Serializer.serialize(comment)
        return Resp(result_code=2000, result_msg="success", data=comment_serialized)

    @swag_from('../swagger/post/comment/create.yaml')
    def post(self):
        if current_user is None:
            return Resp(result_code=2000, result_msg="user is none", data=None)

        user_id = current_user.id
        data = request.get_json()
        post_id = data['post_id']
        comment_content = data['comment_content']
        comment = PostComment(post_id=post_id, comment_content=comment_content, user_id=user_id)
        db.session.add(comment)
        db.session.commit()

        return Resp(result_code=2000, result_msg="success", data=Serializer.serialize(comment))

    @swag_from('../swagger/post/comment/delete.yaml')
    def delete(self, id):
        comment = PostComment.query.filter_by(id=id).first()
        if comment is None:
            return Resp(result_code=2000, result_msg="comment not found", data=None)

        db.session.delete(comment)
        db.session.commit()

        return Resp(result_code=2000, result_msg="success", data=Serializer.serialize(comment))


api.add_resource(
    CommentApi,
    '/comment/<int:id>',
    methods=['GET'],
    endpoint='post/comment/retrieve')
api.add_resource(
    CommentApi,
    '/comment',
    methods=['POST'],
    endpoint='post/comment/create')
# api.add_resource(
#     CommentApi,
#     '/comment/<int:id>',
#     methods=['PUT'],
#     endpoint='post/comment/update')
api.add_resource(
    CommentApi,
    '/comment/<int:id>',
    methods=['DELETE'],
    endpoint='post/comment/delete')


class LikeApi(Resource):
    @swag_from('../swagger/post/like/retrieve.yaml')
    def get(self, id):
        like = PostLike.query.filter_by(id=id).first()
        like_serialized = Serializer.serialize(like)
        return Resp(result_code=2000, result_msg="success", data=like_serialized)

    @swag_from('../swagger/post/like/create.yaml')
    def post(self):
        if current_user is None:
            return Resp(result_code=2000, result_msg="user is none", data=None)

        user_id = current_user.id
        data = request.get_json()
        post_id = data['post_id']
        like = PostLike(post_id=post_id, user_id=user_id)
        db.session.add(like)
        db.session.commit()

        return Resp(result_code=2000, result_msg="success", data=Serializer.serialize(like))

    @swag_from('../swagger/post/like/delete.yaml')
    def delete(self, id):
        like = PostLike.query.filter_by(id=id).first()
        db.session.delete(like)
        db.session.commit()

        return Resp(result_code=2000, result_msg="disliked", data=None)


api.add_resource(
    LikeApi,
    '/like/<int:id>',
    methods=['GET'],
    endpoint='post/like/retrieve')
api.add_resource(
    LikeApi,
    '/like',
    methods=['POST'],
    endpoint='post/like/create')
api.add_resource(
    LikeApi,
    '/like/<int:id>',
    methods=['DELETE'],
    endpoint='post/like/delete')
