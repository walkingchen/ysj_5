from flasgger import swag_from
from flask import Blueprint, request, json, jsonify
from flask_login import current_user
from flask_restful import Api, Resource
from sqlalchemy.orm import load_only

from entity.Resp import Resp
from extensions import db
from models import Post, PostComment, PostLike, Serializer, Timeline, User
from utils import object_as_dict

bp_post = Blueprint('/api/post', __name__)
api = Api(bp_post, '/api/post')

TIMELINE_PUB = 0
TIMELINE_PRI = 1
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
            timeline_id = data['timeline_id']
            post_content = data['post_content']
            type_id = data['type_id']
        except TypeError:
            return json.dumps(Resp(result_code=4000, result_msg='TypeError', data=None).__dict__)
        except KeyError:
            return json.dumps(Resp(result_code=4000, result_msg='KeyError', data=None).__dict__)
        if 'post_title' in data:
            post_title = data['post_title']
        else:
            post_title = None

        post = Post(
            timeline_id=timeline_id,
            post_title=post_title,
            post_content=post_content,
            type_id=type_id,
            user_id=user_id
        )
        db.session.add(post)
        db.session.commit()

        return jsonify(Resp(
            result_code=2000,
            result_msg='success',
            data=Serializer.serialize(post)
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
        data = request.get_json()
        try:
            room_id = data['room_id']
            timeline_type = data['timeline_type']
        except KeyError:
            return json.dumps(Resp(result_code=4000, result_msg='KeyError', data=None).__dict__)
        except TypeError:
            return json.dumps(Resp(result_code=4000, result_msg='TypeError', data=None).__dict__)

        user_id = current_user.id
        if user_id is None:
            return json.dumps(Resp(result_code=4000, result_msg='user id is none', data=None).__dict__)

        # timeline
        if timeline_type == TIMELINE_PUB:
            timeline = Timeline.query.filter_by(room_id=room_id, timeline_type=timeline_type).first()
        elif timeline_type == TIMELINE_PRI:
            timeline = Timeline.query.filter_by(room_id=room_id, timeline_type=timeline_type, user_id=user_id).first()
        else:
            return json.dumps(Resp(result_code=4000, result_msg='timeline_type wrong', data=None).__dict__)

        posts = Post.query.filter_by(timeline_id=timeline.id).limit(MSG_SIZE_INIT).all()
        # 为每篇post添加评论、点赞
        posts_serialized = Serializer.serialize_list(posts)
        process_posts(posts=posts_serialized, user_id=user_id)

        return jsonify(Resp(
            result_code=2000,
            result_msg='success',
            data=posts_serialized
        ).__dict__)


api.add_resource(
    PostApi,
    '/',
    methods=['GET'],
    endpoint='post/list_retrieve')


# 为每篇post添加评论、点赞
def process_posts(posts, user_id):
    for post in posts:
        comments = PostComment.query.filter_by(post_id=post['id']).all()
        comments_serialized = Serializer.serialize_list(comments)
        for comment in comments_serialized:
            user = User.query.filter_by(id=comment['user_id'])\
                .with_entities(User.id, User.username, User.email, User.created_at).first()
            if user is not None:
                comment['user'] = user._asdict()
        post['comments'] = comments_serialized

        likes = PostLike.query.filter_by(post_id=post['id']).all()
        post['likes'] = len(likes)

        # 判断是否已点过赞
        like = PostLike.query.filter_by(post_id=post['id'], user_id=user_id).first()
        if like is None:
            post['liked'] = False
        else:
            post['liked'] = True


class CommentApi(Resource):
    @swag_from('../swagger/post/comment/retrieve.yaml')
    def get(self):
        pass

    @swag_from('../swagger/post/comment/create.yaml')
    def post(self):
        data = request.get_json()
        post_id = data['post_id']

    @swag_from('../swagger/post/comment/delete.yaml')
    def delete(self):
        if 'id' not in request.args:
            pass
        id = request.args['id']
        comment = PostComment.query.filter_by(id=id).first()
        db.session.delete(comment)
        db.session.commit()


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
    def get(self):
        pass

    @swag_from('../swagger/post/like/create.yaml')
    def post(self):
        data = request.get_json()
        post_id = data['post_id']

    @swag_from('../swagger/post/like/delete.yaml')
    def delete(self):
        if 'id' not in request.args:
            pass
        id = request.args['id']
        like = PostLike.query.filter_by(id=id).first()
        db.session.delete(like)
        db.session.commit()


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
# api.add_resource(
#     LikeApi,
#     '/like/<int:id>',
#     methods=['PUT'],
#     endpoint='post/like/update')
api.add_resource(
    LikeApi,
    '/like/<int:id>',
    methods=['DELETE'],
    endpoint='post/like/delete')
