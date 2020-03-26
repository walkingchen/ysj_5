from flask import Blueprint, request
from flask_restful import Api, Resource

from extensions import db
from models import Post, PostComment, PostLike

bp_post = Blueprint('/post', __name__)
api = Api(bp_post, '/post')


class PostApi(Resource):
    def get(self):
        """
        ---
        tags:
          - Post
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
        data = request.get_json()
        timeline_id = data['timeline_id']

    def post(self):
        """
        ---
        tags:
          - Post
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


class CommentApi(Resource):
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


class LikeApi(Resource):
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