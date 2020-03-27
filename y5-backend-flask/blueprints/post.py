from flasgger import swag_from
from flask import Blueprint, request
from flask_restful import Api, Resource

from extensions import db
from models import Post, PostComment, PostLike

bp_post = Blueprint('/post', __name__)
api = Api(bp_post, '/post')


class PostApi(Resource):
    @swag_from('../swagger/post/retrieve.yaml')
    def get(self):
        data = request.get_json()
        timeline_id = data['timeline_id']

    @swag_from('../swagger/post/create.yaml')
    def post(self):
        data = request.get_json()
        timeline_id = data['timeline_id']
        if 'post_title' in data:
            post_title = data['post_title']
        post_content = data['post_content']
        type_id = data['type_id']
        user_id = ''  # fixme

    @swag_from('../swagger/post/delete.yaml')
    def delete(self):
        if 'id' not in request.args:
            pass
        id = request.args['id']
        post = Post.query.filter_by(id=id).first()
        db.session.delete(post)
        db.session.commit()


api.add_resource(
    PostApi,
    '/post/<int:id>',
    methods=['GET'],
    endpoint='post/retrieve')
api.add_resource(
    PostApi,
    '/member',
    methods=['POST'],
    endpoint='post/create')
api.add_resource(
    PostApi,
    '/member/<int:id>',
    methods=['PUT'],
    endpoint='post/update')
api.add_resource(
    PostApi,
    '/post/<int:id>',
    methods=['DELETE'],
    endpoint='post/delete')


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
    '/post/comment/<int:id>',
    methods=['GET'],
    endpoint='post/comment/retrieve')
api.add_resource(
    CommentApi,
    '/post/comment',
    methods=['POST'],
    endpoint='post/comment/create')
api.add_resource(
    CommentApi,
    '/post/comment/<int:id>',
    methods=['PUT'],
    endpoint='post/comment/update')
api.add_resource(
    CommentApi,
    '/post/comment/<int:id>',
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
    '/post/like/<int:id>',
    methods=['GET'],
    endpoint='post/like/retrieve')
api.add_resource(
    LikeApi,
    '/post/like',
    methods=['POST'],
    endpoint='post/like/create')
api.add_resource(
    LikeApi,
    '/post/like/<int:id>',
    methods=['PUT'],
    endpoint='post/like/update')
api.add_resource(
    CommentApi,
    '/post/like/<int:id>',
    methods=['DELETE'],
    endpoint='post/like/delete')
