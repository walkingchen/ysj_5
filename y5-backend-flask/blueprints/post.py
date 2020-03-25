from flask import Blueprint, request
from flask_restful import Api

from extensions import db
from models import Post, PostComment, PostLike

bp_post = Blueprint('/', __name__)
api = Api(bp_post, '/post')


class PostApi:
    def get(self):
        pass

    def post(self):
        data = request.get_json()
        timeline_id = data['timeline_id']
        if 'post_title' in data:
            post_title = data['post_title']
        post_content = data['post_content']
        type_id = data['type_id']
        user_id = ''  # fixme

    def delete(self):
        if 'id' not in request.args:
            pass
        id = request.args['id']
        post = Post.query.filter_by(id=id).first()
        db.session.delete(post)
        db.session.commit()


api.add_resource(PostApi, '/<int:id>')


class CommentApi:
    def get(self):
        pass

    def post(self):
        data = request.get_json()
        post_id = data['post_id']

    def delete(self):
        if 'id' not in request.args:
            pass
        id = request.args['id']
        comment = PostComment.query.filter_by(id=id).first()
        db.session.delete(comment)
        db.session.commit()


api.add_resource(CommentApi, '/<int:id>')


class LikeApi:
    def get(self):
        pass

    def post(self):
        data = request.get_json()
        post_id = data['post_id']

    def delete(self):
        if 'id' not in request.args:
            pass
        id = request.args['id']
        like = PostLike.query.filter_by(id=id).first()
        db.session.delete(like)
        db.session.commit()


api.add_resource(LikeApi, '/<int:id>')