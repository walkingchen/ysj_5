import csv
import io
import os
import time
import zipfile

from flasgger import swag_from
from flask import Blueprint, request, json, jsonify, current_app
from flask_login import current_user, login_required
from flask_restful import Api, Resource
from sqlalchemy.orm.exc import ObjectDeletedError

import config
from entity.Resp import Resp
from extensions import db, socketio
from models import PublicPost, PostComment, PostLike, Serializer, Timeline, User, Room, RoomPrototype, RoomMember, \
    PostFactcheck, PostFlag, SystemMessage, Photo, PostStatus, Redspot, CommentFlag, CommentLike, PrivateMessage, \
    PrivatePost, SystemPost, PollPost
from service import get_friends, process_posts, process_post
from utils import rename_image, resize_image

bp_post = Blueprint('/api/post', __name__)
api = Api(bp_post, '/api/post')


MSG_SIZE_INIT = 5


class PostApi(Resource):
    @swag_from('../swagger/post/retrieve.yaml')
    def get(self, id):
        if not current_user.is_authenticated:
            return jsonify(Resp(result_code=4001, result_msg='need to login', data=None).__dict__)

        user_id = current_user.id

        post = PublicPost.query.get(id)
        if post is None:
            return jsonify(Resp(
                result_code=4000,
                result_msg='post not found',
                data=None
            ).__dict__)

        post_serialized = Serializer.serialize(post)
        process_post(post_serialized, user_id)

        return jsonify(Resp(
            result_code=2000,
            result_msg='success',
            data=post_serialized
        ).__dict__)

    @swag_from('../swagger/post/create.yaml')
    def post(self):
        if not current_user.is_authenticated:
            return jsonify(Resp(result_code=4001, result_msg='need to login', data=None).__dict__)

        user_id = current_user.id
        data = request.get_json()
        try:
            timeline_type = int(data['timeline_type'])
            post_content = data['post_content']
            post_type = int(data['post_type'])
            room_id = data['room_id']
            sid = data['sid']
            topic = int(data['topic'])
        except TypeError:
            return jsonify(Resp(result_code=4000, result_msg='TypeError', data=None).__dict__)
        except KeyError:
            return jsonify(Resp(result_code=4000, result_msg='KeyError', data=None).__dict__)

        if 'post_title' in data:
            post_title = data['post_title']
        else:
            post_title = None
        if 'keywords' in data:
            keywords = data['keywords']
        else:
            keywords = None
        if 'post_shared_id' in data:
            post_shared_id = data['post_shared_id']
        else:
            post_shared_id = None
        if 'photo_uri' in data:
            photo_uri = data['photo_uri']
        else:
            photo_uri = None
        if 'message_id' in data:
            message_id = data['message_id']
        else:
            message_id = None

        post = PublicPost(
            timeline_type=timeline_type,
            post_title=post_title,
            post_content=post_content,
            keywords=keywords,
            post_type=post_type,
            user_id=user_id,
            room_id=room_id,
            post_shared_id=post_shared_id,
            topic=topic,
            photo_uri=photo_uri,
            message_id=message_id
        )
        db.session.add(post)
        db.session.commit()

        # 将private message设置为已分享
        if post_shared_id is not None:
            post_shared = PrivatePost.query.filter_by(id=post_shared_id).first()
            post_shared.timeline_type = 2
            db.session.commit()

        room = Room.query.filter_by(id=room_id).first()
        friends = get_friends(room=room, user_id=user_id)
        for friend in friends:
            redspot = Redspot.query.filter_by(room_id=room_id, user_id=friend.user_id, topic=topic).first()
            if redspot is None:
                redspot = Redspot(
                    room_id=room_id,
                    user_id=friend.user_id,
                    topic=topic,
                    unread=1
                )
                db.session.add(redspot)
            else:
                redspot.unread += 1
            db.session.commit()

        socketio.emit('post_pull',
                      {
                          'timeline_type': timeline_type,
                          'posts_number': 1,
                          'topic': topic
                      },
                      room_id=post.room_id,
                      skip_sid=sid)

        return jsonify(Resp(
            result_code=2000,
            result_msg='success',
            data=Serializer.serialize(post)
        ).__dict__)

    @swag_from('../swagger/post/update.yaml')
    def put(self, id):
        return jsonify(Resp(
            result_code=2000,
            result_msg='success',
            data=None
        ).__dict__)

    @swag_from('../swagger/post/delete.yaml')
    def delete(self, id):
        if not current_user.is_authenticated:
            return jsonify(Resp(result_code=4001, result_msg='need to login', data=None).__dict__)

        post = PublicPost.query.get(id)
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
    '',
    methods=['POST'],
    endpoint='post/create')
# api.add_resource(
#     PostApi,
#     '/<int:id>',
#     methods=['PUT'],
#     endpoint='post/update')
api.add_resource(
    PostApi,
    '/<int:id>',
    methods=['DELETE'],
    endpoint='post/delete')


class PostListApi(Resource):
    @swag_from('../swagger/post/list_retrieve.yaml')
    def get(self):
        if not current_user.is_authenticated:
            return jsonify(Resp(result_code=4001, result_msg='need to login', data=None).__dict__)

        data = request.args
        try:
            room_id = int(data['room_id'])
            timeline_type = int(data['timeline_type'])
            topic = int(data['topic'])
        except KeyError:
            return jsonify(Resp(result_code=4000, result_msg='KeyError', data=None).__dict__)
        except TypeError:
            return jsonify(Resp(result_code=4000, result_msg='TypeError', data=None).__dict__)

        if 'last_update' in data:
            last_update = data['last_update']
        else:
            last_update = None

        user_id = current_user.id
        if user_id is None:
            return jsonify(Resp(result_code=4000, result_msg='user id is none', data=None).__dict__)

        room = Room.query.filter_by(id=room_id).first()
        friends = get_friends(room=room, user_id=user_id)

        friend_ids = [user_id]  # 用于timeline显示添加用户自己的posts
        for friend in friends:
            friend_ids.append(friend.user_id)

        if timeline_type == config.TIMELINE_PUB:
            if last_update is not None:
                posts = PublicPost.query.filter(
                    PublicPost.room_id == room_id,
                    PublicPost.user_id.in_(friend_ids),
                    PublicPost.timeline_type == timeline_type,
                    PublicPost.topic == topic,
                    PublicPost.updated_at > last_update,
                    PublicPost.is_system_post.is_(None)  # fixme
                ).order_by(PublicPost.created_at.desc()).all()
            else:
                posts = PublicPost.query.filter(
                    PublicPost.room_id == room_id,
                    PublicPost.user_id.in_(friend_ids),
                    PublicPost.timeline_type == timeline_type,
                    PublicPost.topic == topic,
                    PublicPost.is_system_post.is_(None)  # fixme
                ).order_by(PublicPost.created_at.desc()).all()
        else:   # 获取private message feed
            posts = PrivatePost.query.filter(
                PrivatePost.room_id == room_id,
                PrivatePost.user_id == user_id,
                PrivatePost.topic == topic,
                # PrivatePost.created_at > last_update
            ).order_by(PrivatePost.created_at.desc()).all()

        # 为每篇post添加评论、点赞
        posts_serialized = Serializer.serialize_list(posts)
        process_posts(posts=posts_serialized, user_id=user_id)

        unread_list = []
        read_list = []
        for post in posts_serialized:
            if post['read_status'] is False or post['comments_all_read'] is False:
                unread_list.append(post)
            else:
                read_list.append(post)
        all_posts = unread_list + read_list

        redspot = Redspot.query.filter_by(room_id=room_id, user_id=current_user.id, topic=topic).first()
        if redspot is None:
            redspot = Redspot(
                room_id=room_id,
                user_id=current_user.id,
                topic=topic,
                unread=0
            )
            db.session.add(redspot)
        else:
            redspot.unread = 0
        db.session.commit()

        return jsonify(Resp(result_code=2000, result_msg='success', data=all_posts).__dict__)


api.add_resource(
    PostListApi,
    '',
    methods=['GET'],
    endpoint='post/list_retrieve')


class PrivatePostApi(Resource):
    @swag_from('../swagger/post/private_post/retrieve.yaml')
    def get(self, id):
        if not current_user.is_authenticated:
            return jsonify(Resp(result_code=4001, result_msg='need to login', data=None).__dict__)

        user_id = current_user.id

        post = PrivatePost.query.get(id)
        if post is None:
            return jsonify(Resp(
                result_code=4000,
                result_msg='post not found',
                data=None
            ).__dict__)

        post_serialized = Serializer.serialize(post)
        process_post(post_serialized, user_id)

        return jsonify(Resp(
            result_code=2000,
            result_msg='success',
            data=post_serialized
        ).__dict__)


api.add_resource(
    PrivatePostApi,
    '/private_post/<int:id>',
    methods=['GET'],
    endpoint='post/private_post/retrieve')


# class PrivatePostListApi(Resource):
#     @swag_from('../swagger/post/private_post/list_retrieve.yaml')
#     def get(self):
#         data = request.args
#         try:
#             room_id = data['room_id']
#             topic = data['topic']
#         except TypeError:
#             return jsonify(Resp(result_code=4000, result_msg='TypeError', data=None).__dict__)
#         except KeyError:
#             return jsonify(Resp(result_code=4000, result_msg='KeyError', data=None).__dict__)
#
#         messages = PrivatePost.query.filter_by(room_id=room_id, topic=topic).all()      # list not first, for api
#
#         message_serialized_list = []
#         for message in messages:
#             message_serialized = Serializer.serialize(message)
#             process_post(message_serialized, current_user.id)
#
#         resp = Resp(
#             result_code=2000,
#             result_msg="success",
#             data=message_serialized_list
#         )
#
#         return jsonify(resp.__dict__)
#
#
# api.add_resource(
#     PrivatePostListApi,
#     '/private_post',
#     methods=['GET'],
#     endpoint='post/private_post/list_retrieve')


class SystemMessageApi(Resource):
    @swag_from('../swagger/post/daily/retrieve.yaml')
    def get(self):
        data = request.args
        try:
            room_id = data['room_id']
            topic = data['topic']
        except TypeError:
            return jsonify(Resp(result_code=4000, result_msg='TypeError', data=None).__dict__)
        except KeyError:
            return jsonify(Resp(result_code=4000, result_msg='KeyError', data=None).__dict__)

        messages = PublicPost.query.filter_by(
            room_id=room_id,
            topic=topic,
            is_system_post=1
        ).all()

        message_serialized_list = []
        for message in messages:
            message_serialized = Serializer.serialize(message)
            process_post(message_serialized, current_user.id)
            message_serialized_list.append(message_serialized)

        resp = Resp(
            result_code=2000,
            result_msg="success",
            data=message_serialized_list
        )

        return jsonify(resp.__dict__)


api.add_resource(
    SystemMessageApi,
    '/system_post',
    methods=['GET'],
    endpoint='post/system_post/retrieve')


class UploadApi(Resource):
    @swag_from('../swagger/post/photo/create.yaml')
    def post(self):
        if request.method == 'POST' and 'file' in request.files:
            f = request.files.get('file')
            filename = rename_image(f.filename)
            f.save(os.path.join(current_app.config['UPLOAD_PATH'], filename))
            filename_s = resize_image(f, filename, current_app.config['PHOTO_SIZE']['small'])
            filename_m = resize_image(f, filename, current_app.config['PHOTO_SIZE']['medium'])
            photo = Photo(
                filename=filename,
                filename_s=filename_s,
                filename_m=filename_m,
                author_id=current_user.id
            )
            db.session.add(photo)
            db.session.commit()

            photo_serialized = Serializer.serialize(photo)
            photo_serialized['upload_path'] = '/uploads/'

            return jsonify(Resp(result_code=2000, result_msg="success", data=photo_serialized).__dict__)

        return jsonify(Resp(result_code=4000, result_msg="param error?", data=None).__dict__)


api.add_resource(
    UploadApi,
    '/photo',
    methods=['POST'],
    endpoint='post/photo/create')


class TopicApi(Resource):
    @swag_from('../swagger/post/topic/list_retrieve.yaml')
    def get(self):
        data = request.args
        try:
            room_id = data['room_id']
        except TypeError:
            return jsonify(Resp(result_code=4000, result_msg='TypeError', data=None).__dict__)
        except KeyError:
            return jsonify(Resp(result_code=4000, result_msg='KeyError', data=None).__dict__)

        # get topics
        room = Room.query.get(room_id)
        updated_at = room.updated_at
        local_time = time.localtime(int(updated_at.timestamp()))
        activated_day = local_time.tm_yday
        activated_year = local_time.tm_year
        print('activated_day = ' + str(activated_day))

        now = time.localtime(time.time())
        now_day = now.tm_yday
        now_year = now.tm_year
        print('now_day = ' + str(now_day))

        if now_year > activated_year:
            n = now_day + 365 - activated_day + 1
        else:
            n = now_day - activated_day + 1

        if n > 8:
            n = 8

        data = []
        for i in range(n):
            topic = i + 1
            redspot = Redspot.query.filter_by(room_id=room_id, user_id=current_user.id, topic=topic).first()
            if redspot is None:
                data.append({'topic': topic, 'redspot': False})
                redspot = Redspot(
                    room_id=room_id,
                    user_id=current_user.id,
                    topic=topic,
                    unread=0
                )
                db.session.add(redspot)
            else:
                if redspot.unread == 0:
                    data.append({'topic': topic, 'redspot': False})
                else:
                    data.append({'topic': topic, 'redspot': True})
                # redspot.unread = 0    获取topic list时不需要重置，获取post list时才需要
            db.session.commit()

        return jsonify(Resp(result_code=2000, result_msg="success", data=data).__dict__)


api.add_resource(
    TopicApi,
    '/topic',
    methods=['GET'],
    endpoint='post/topic/list_retrieve')


class CommentApi(Resource):
    @swag_from('../swagger/post/comment/retrieve.yaml')
    def get(self, id):
        comment = PostComment.query.get(id)
        comment_serialized = Serializer.serialize(comment)
        resp = Resp(
            result_code=2000,
            result_msg="success",
            data=comment_serialized
        )
        return jsonify(resp.__dict__)

    @swag_from('../swagger/post/comment/create.yaml')
    def post(self):
        if not current_user.is_authenticated:
            return jsonify(Resp(result_code=4001, result_msg='need to login', data=None).__dict__)

        user_id = current_user.id
        data = request.get_json()
        try:
            post_id = data['post_id']
            comment_content = data['comment_content']
            sid = data['sid']
        except KeyError:
            return jsonify(Resp(result_code=4000, result_msg='KeyError', data=None).__dict__)

        comment = PostComment(post_id=post_id, comment_content=comment_content, user_id=user_id)
        db.session.add(comment)
        db.session.commit()

        post = PublicPost.query.get(post_id)
        socketio.emit('comment_pull',
                      {
                          'topic': post.topic,
                          'post_id': post_id,
                          'comment_id': comment.id
                      },
                      room_id=post.room_id,
                      skip_sid=sid)

        room = Room.query.filter_by(id=post.room_id).first()
        friends = get_friends(room=room, user_id=user_id)
        for friend in friends:
            redspot = Redspot.query.filter_by(room_id=post.room_id, user_id=friend.user_id, topic=post.topic).first()
            if redspot is None:
                redspot = Redspot(
                    room_id=post.room_id,
                    user_id=friend.user_id,
                    topic=post.topic,
                    unread=1
                )
                db.session.add(redspot)
            else:
                redspot.unread += 1
            db.session.commit()

        return jsonify(Resp(result_code=2000, result_msg="success", data=Serializer.serialize(comment)).__dict__)

    @swag_from('../swagger/post/comment/delete.yaml')
    def delete(self, id):
        comment = PostComment.query.get(id)
        if comment is None:
            return jsonify(Resp(result_code=2000, result_msg="comment not found", data=None).__dict__)

        db.session.delete(comment)
        db.session.commit()

        return jsonify(Resp(result_code=2000, result_msg="success", data=Serializer.serialize(comment)).__dict__)


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
api.add_resource(
    CommentApi,
    '/comment/<int:id>',
    methods=['DELETE'],
    endpoint='post/comment/delete')


class LikeApi(Resource):
    @swag_from('../swagger/post/like/retrieve.yaml')
    def get(self, id):
        like = PostLike.query.get(id)
        like_serialized = Serializer.serialize(like)
        return jsonify(Resp(result_code=2000, result_msg="success", data=like_serialized).__dict__)

    @swag_from('../swagger/post/like/create.yaml')
    def post(self):
        if not current_user.is_authenticated:
            return jsonify(Resp(result_code=4001, result_msg='need to login', data=None).__dict__)

        user_id = current_user.id
        data = request.get_json()
        try:
            post_id = data['post_id']
            like_or_not = int(data['like_or_not'])
        except KeyError:
            return jsonify(Resp(result_code=4000, result_msg='KeyError', data=None).__dict__)
        except TypeError:
            return jsonify(Resp(result_code=4000, result_msg='TypeError', data=None).__dict__)

        like = PostLike(post_id=post_id, user_id=user_id, post_like=like_or_not)
        db.session.add(like)
        db.session.commit()

        return jsonify(Resp(result_code=2000, result_msg="success", data=Serializer.serialize(like)).__dict__)

    @swag_from('../swagger/post/like/update.yaml')
    def put(self, id):
        if not current_user.is_authenticated:
            return jsonify(Resp(result_code=4001, result_msg='need to login', data=None).__dict__)

        user_id = current_user.id
        data = request.get_json()
        like_or_not = data['like_or_not']
        like = PostLike.query.filter_by(id=id, user_id=user_id).first()
        like.post_like = like_or_not
        db.session.commit()

        return jsonify(Resp(result_code=2000, result_msg="success", data=Serializer.serialize(like)).__dict__)

    @swag_from('../swagger/post/like/delete.yaml')
    def delete(self, id):
        like = PostLike.query.get(id)
        db.session.delete(like)
        db.session.commit()

        return jsonify(Resp(result_code=2000, result_msg="disliked", data=None).__dict__)


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
    methods=['PUT'],
    endpoint='post/like/update')
api.add_resource(
    LikeApi,
    '/like/<int:id>',
    methods=['DELETE'],
    endpoint='post/like/delete')


class CommentLikeApi(Resource):
    @swag_from('../swagger/post/comment/like/retrieve.yaml')
    def get(self, id):
        like = CommentLike.query.get(id)
        like_serialized = Serializer.serialize(like)
        return jsonify(Resp(result_code=2000, result_msg="success", data=like_serialized).__dict__)

    @swag_from('../swagger/post/comment/like/create.yaml')
    def post(self):
        if not current_user.is_authenticated:
            return jsonify(Resp(result_code=4001, result_msg='need to login', data=None).__dict__)

        user_id = current_user.id
        data = request.get_json()
        try:
            comment_id = data['comment_id']
            like_or_not = int(data['like_or_not'])
        except KeyError:
            return jsonify(Resp(result_code=4000, result_msg='KeyError', data=None).__dict__)
        except TypeError:
            return jsonify(Resp(result_code=4000, result_msg='TypeError', data=None).__dict__)

        like = CommentLike(comment_id=comment_id, user_id=user_id, comment_like=like_or_not)
        db.session.add(like)
        db.session.commit()

        return jsonify(Resp(result_code=2000, result_msg="success", data=Serializer.serialize(like)).__dict__)

    @swag_from('../swagger/post/comment/like/update.yaml')
    def put(self, id):
        if not current_user.is_authenticated:
            return jsonify(Resp(result_code=4001, result_msg='need to login', data=None).__dict__)

        user_id = current_user.id
        data = request.get_json()
        like_or_not = data['like_or_not']
        like = CommentLike.query.filter_by(id=id, user_id=user_id).first()
        like.comment_like = like_or_not
        db.session.commit()

        return jsonify(Resp(result_code=2000, result_msg="success", data=Serializer.serialize(like)).__dict__)

    @swag_from('../swagger/post/comment/like/delete.yaml')
    def delete(self, id):
        like = CommentLike.query.get(id)
        db.session.delete(like)
        db.session.commit()

        return jsonify(Resp(result_code=2000, result_msg="disliked", data=None).__dict__)


api.add_resource(
    CommentLikeApi,
    '/comment/like/<int:id>',
    methods=['GET'],
    endpoint='post/comment/like/retrieve')
api.add_resource(
    CommentLikeApi,
    '/comment/like',
    methods=['POST'],
    endpoint='post/comment/like/create')
api.add_resource(
    CommentLikeApi,
    '/comment/like/<int:id>',
    methods=['PUT'],
    endpoint='post/comment/like/update')
api.add_resource(
    CommentLikeApi,
    '/comment/like/<int:id>',
    methods=['DELETE'],
    endpoint='post/comment/like/delete')


class FactcheckApi(Resource):
    @swag_from('../swagger/post/factcheck/retrieve.yaml')
    def get(self, id):
        check = PostFactcheck.query.get(id)
        check_serialized = Serializer.serialize(check)
        return jsonify(Resp(result_code=2000, result_msg="success", data=check_serialized).__dict__)

    @swag_from('../swagger/post/factcheck/create.yaml')
    def post(self):
        if not current_user.is_authenticated:
            return jsonify(Resp(result_code=4001, result_msg='need to login', data=None).__dict__)

        user_id = current_user.id
        data = request.get_json()
        try:
            post_id = data['post_id']
        except KeyError:
            return jsonify(Resp(result_code=4000, result_msg='KeyError', data=None).__dict__)
        check = PostFactcheck(post_id=post_id, user_id=user_id)
        db.session.add(check)
        db.session.commit()

        return jsonify(Resp(result_code=2000, result_msg="success", data=Serializer.serialize(check)).__dict__)

    @swag_from('../swagger/post/factcheck/delete.yaml')
    def delete(self, id):
        check = PostFactcheck.query.get(id)
        db.session.delete(check)
        db.session.commit()

        return jsonify(Resp(result_code=2000, result_msg="submitted", data=None).__dict__)


api.add_resource(
    FactcheckApi,
    '/factcheck/<int:id>',
    methods=['GET'],
    endpoint='post/factcheck/retrieve')
api.add_resource(
    FactcheckApi,
    '/factcheck',
    methods=['POST'],
    endpoint='post/factcheck/create')
api.add_resource(
    FactcheckApi,
    '/factcheck/<int:id>',
    methods=['DELETE'],
    endpoint='post/factcheck/delete')


class FlagApi(Resource):
    @swag_from('../swagger/post/flag/retrieve.yaml')
    def get(self, id):
        flag = PostFlag.query.get(id)
        flag_serialized = Serializer.serialize(flag)
        return jsonify(Resp(result_code=2000, result_msg="success", data=flag_serialized).__dict__)

    @swag_from('../swagger/post/flag/create.yaml')
    def post(self):
        if not current_user.is_authenticated:
            return jsonify(Resp(result_code=4001, result_msg='need to login', data=None).__dict__)

        user_id = current_user.id
        data = request.get_json()
        try:
            post_id = data['post_id']
        except KeyError:
            return jsonify(Resp(result_code=4000, result_msg='KeyError', data=None).__dict__)
        flag = PostFlag(post_id=post_id, user_id=user_id, flag=1)
        db.session.add(flag)
        db.session.commit()

        return jsonify(Resp(result_code=2000, result_msg="success", data=Serializer.serialize(flag)).__dict__)

    @swag_from('../swagger/post/flag/delete.yaml')
    def delete(self, id):
        flag = PostFlag.query.get(id)
        db.session.delete(flag)
        db.session.commit()

        return jsonify(Resp(result_code=2000, result_msg="submitted", data=None).__dict__)


api.add_resource(
    FlagApi,
    '/flag/<int:id>',
    methods=['GET'],
    endpoint='post/flag/retrieve')
api.add_resource(
    FlagApi,
    '/flag',
    methods=['POST'],
    endpoint='post/flag/create')
api.add_resource(
    FlagApi,
    '/flag/<int:id>',
    methods=['DELETE'],
    endpoint='post/flag/delete')


class CommentFlagApi(Resource):
    @swag_from('../swagger/post/comment/flag/retrieve.yaml')
    def get(self, id):
        flag = CommentFlag.query.get(id)
        flag_serialized = Serializer.serialize(flag)
        return jsonify(Resp(result_code=2000, result_msg="success", data=flag_serialized).__dict__)

    @swag_from('../swagger/post/comment/flag/create.yaml')
    def post(self):
        if not current_user.is_authenticated:
            return jsonify(Resp(result_code=4001, result_msg='need to login', data=None).__dict__)

        user_id = current_user.id
        data = request.get_json()
        try:
            comment_id = data['comment_id']
        except KeyError:
            return jsonify(Resp(result_code=4000, result_msg='KeyError', data=None).__dict__)
        flag = CommentFlag(comment_id=comment_id, user_id=user_id)
        db.session.add(flag)
        db.session.commit()

        return jsonify(Resp(result_code=2000, result_msg="success", data=Serializer.serialize(flag)).__dict__)

    @swag_from('../swagger/post/comment/flag/delete.yaml')
    def delete(self, id):
        flag = CommentFlag.query.get(id)
        db.session.delete(flag)
        db.session.commit()

        return jsonify(Resp(result_code=2000, result_msg="submitted", data=None).__dict__)


api.add_resource(
    CommentFlagApi,
    '/comment/flag/<int:id>',
    methods=['GET'],
    endpoint='post/comment/flag/retrieve')
api.add_resource(
    CommentFlagApi,
    '/comment/flag',
    methods=['POST'],
    endpoint='post/comment/flag/create')
api.add_resource(
    CommentFlagApi,
    '/comment/flag/<int:id>',
    methods=['DELETE'],
    endpoint='post/comment/flag/delete')


# Daily Poll
class DailyPollApi(Resource):
    @swag_from('../swagger/post/poll/retrieve.yaml')
    def get(self):
        data = request.args
        try:
            room_id = data['room_id']
            topic = data['topic']
        except TypeError:
            return jsonify(Resp(result_code=4000, result_msg='TypeError', data=None).__dict__)
        except KeyError:
            return jsonify(Resp(result_code=4000, result_msg='KeyError', data=None).__dict__)

        message = PollPost.query.filter_by(
            room_id=room_id,
            topic=topic
        ).first()

        if message is not None:
            message_serialized = Serializer.serialize(message)
            if 'photo_uri' in message_serialized:
                message_serialized['photo_uri'] = '/uploads/' + message_serialized['photo_uri']

        else:
            message_serialized = {'photo_uri': '/uploads/daily_poll.jpeg'}

        resp = Resp(
            result_code=2000,
            result_msg="success",
            data=message_serialized
        )

        return jsonify(resp.__dict__)


api.add_resource(
    DailyPollApi,
    '/daily_poll',
    methods=['GET'],
    endpoint='post/daily_poll/retrieve')


# import private messages pool
@swag_from('../swagger/post/import_private_messages.yaml')
@bp_post.route('/api/post/import_private_messages_pool', methods=['POST'])
def import_private_messages():
    file = request.files['file']
    stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
    csv_input = csv.reader(stream)

    # 清空pool
    # messages_exisited = PrivateMessage.query.all()
    # for message in messages_exisited:
    #     try:
    #         db.session.delete(message)
    #         db.session.commit()
    #     except ObjectDeletedError as e:
    #         print('message already deleted')

    for key, line in enumerate(csv_input):
        if key == 0:
            if line != ['id', 'message_id', 'message_title', 'message_summary', 'message_content', 'photo_uri']:
                return jsonify(Resp(result_code=4000, result_msg="error content", data=None).__dict__)
            continue

        message_id = line[1]
        message_title = line[2]
        abstract = line[3]
        message_content = line[4]
        photo_uri = line[5]

        private_message = PrivateMessage(
            message_id=message_id,
            message_title=message_title,
            message_content=message_content,
            photo_uri=photo_uri,
            abstract=abstract,
        )
        db.session.add(private_message)
        db.session.commit()

    return jsonify(Resp(result_code=2000, result_msg="success", data=None).__dict__)


# assign private message
@swag_from('../swagger/post/import_members_with_messages.yaml')
@bp_post.route('/api/post/import_private_messages_assign', methods=['POST'])
def import_members_with_messages():
    file = request.files['file']
    stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
    csv_input = csv.reader(stream)

    room_cleaned = []
    for key, line in enumerate(csv_input):
        if key == 0:
            if line != ['id', 'user_id', 'room_type', 'room_id', 'seat_no', 'day', 'topic_no', 'message_id']:
                return jsonify(Resp(result_code=4000, result_msg="error content", data=None).__dict__)
            continue
        # id,user_id,room_type,room_id,seat_no,day,topic_no,message_id
        user_id = line[1]
        room_id = line[3]
        seat_no = line[4]
        day = line[5]
        topic_no = line[6]
        message_id = line[7]

        # clean by room_id, ignore if activated
        if room_id not in room_cleaned:
            room = Room.query.filter_by(id=room_id).first()     # id, not room_id
            if room.activated == 1:
                return jsonify(Resp(result_code=4000, result_msg="room activated", data=room.serialize()).__dict__)
            messages_existed = PrivatePost.query.filter_by(room_id=room_id).all()
            for message in messages_existed:
                db.session.delete(message)
                db.session.commit()
            room_cleaned.append(room_id)

        user = User.query.filter_by(id=user_id).first()
        if user is None:
            return jsonify(Resp(result_code=4000, result_msg="username error", data=None).__dict__)

        member = RoomMember.query.filter_by(user_id=user.id, room_id=room_id).first()
        if member is None:
            member = RoomMember(
                user_id=user.id,
                room_id=room_id,
                seat_no=seat_no
            )
            db.session.add(member)
            db.session.commit()

        participant = User.query.filter_by(id=user.id).first()
        private_message = PrivateMessage.query.filter_by(message_id=message_id).first()
        if private_message is None:
            return jsonify(Resp(result_code=4000, result_msg="message id not exists, id=" + str(message_id), data=None).__dict__)

        post = PrivatePost(
            message_id=message_id,
            timeline_type=config.TIMELINE_PRI,
            post_title=private_message.message_title,
            post_content=private_message.message_content,
            abstract=private_message.abstract,
            post_type=1,    # fixme
            user_id=participant.id,
            room_id=room_id,
            topic=topic_no,
            photo_uri=private_message.photo_uri
        )
        db.session.add(post)
        db.session.commit()

    return jsonify(Resp(result_code=2000, result_msg="success", data=None).__dict__)


# upload system message pool
@swag_from('../swagger/post/import_post_daily_pool.yaml')
@bp_post.route('/api/post/import_system_message_pool', methods=['POST'])
def import_post_daily_pool():
    file = request.files['file']
    stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
    csv_input = csv.reader(stream)

    # 清空pool
    messages_exisited = SystemMessage.query.all()
    for message in messages_exisited:
        db.session.delete(message)
        db.session.commit()

    for key, line in enumerate(csv_input):
        if key == 0:
            if line != ['id', 'message_id', 'message_title', 'message_summary', 'message_content', 'photo_uri']:
                return jsonify(Resp(result_code=4000, result_msg="error content", data=None).__dict__)
            continue

        message_id = line[1]
        message_title = line[2]
        abstract = line[3]
        message_content = line[4]
        photo_uri = line[5]

        system_message = SystemMessage(
            message_id=message_id,
            message_title=message_title,
            message_content=message_content,
            photo_uri=photo_uri,
            abstract=abstract,
        )
        db.session.add(system_message)
        db.session.commit()

    return jsonify(Resp(result_code=2000, result_msg="success", data=None).__dict__)


# assign system message
@swag_from('../swagger/post/import_post_daily.yaml')
@bp_post.route('/api/post/import_system_message_assign', methods=['POST'])
def import_post_daily_by_room():
    file = request.files['file']
    stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
    csv_input = csv.reader(stream)
    room_cleaned = []
    for key, line in enumerate(csv_input):
        if key == 0:
            if line != ['id', 'room_id', 'day', 'topic_no', 'message_id']:
                return jsonify(Resp(result_code=4000, result_msg="error content", data=None).__dict__)
            continue
        room_id = line[1]
        topic = line[2]     # day
        message_id = line[4]

        # clean by room_id
        if room_id not in room_cleaned:
            room = Room.query.filter_by(id=room_id).first()  # id, not room_id
            if room.activated == 1:
                return jsonify(Resp(result_code=4000, result_msg="room activated, room id: " + str(room_id), data=room.serialize()).__dict__)
            messages_existed = PublicPost.query.filter_by(room_id=room_id, is_system_post=1).all()
            for message in messages_existed:
                db.session.delete(message)
                db.session.commit()
            room_cleaned.append(room_id)

        system_message = SystemMessage.query.filter_by(message_id=message_id).first()
        post = PublicPost(
            message_id=message_id,
            # timeline_type=config.TIMELINE_PRI,
            post_title=system_message.message_title,
            post_content=system_message.message_content,
            abstract=system_message.abstract,
            post_type=1,  # fixme
            user_id=current_user.id,    # added 2022.02.19
            room_id=room_id,
            topic=topic,
            photo_uri=system_message.photo_uri,
            is_system_post=1
        )
        db.session.add(post)
        db.session.commit()

    return jsonify(Resp(result_code=2000, result_msg="success added to public post", data=None).__dict__)


@swag_from('../swagger/post/photo/import_private_messages_pics.yaml')
@bp_post.route('/api/post/photo/import_private_messages_pool_pics', methods=['POST'])
def import_private_messages_pics():
    file = request.files['file']
    ext = file.filename.split('.')[-1]
    filename = os.path.join(config.UPLOAD_PATH, 'private_messages_pics.' + ext)
    file.save(filename)

    with zipfile.ZipFile(filename, "r") as z:
        z.extractall(config.UPLOAD_PATH)

    return jsonify(Resp(result_code=2000, result_msg="success", data=None).__dict__)


@swag_from('../swagger/post/photo/import_system_messages_pics.yaml')
@bp_post.route('/api/post/photo/import_system_messages_pool_pics', methods=['POST'])
def import_system_messages_pics():
    file = request.files['file']
    ext = file.filename.split('.')[-1]
    filename = os.path.join(config.UPLOAD_PATH, 'system_messages_pics.' + ext)
    file.save(filename)

    with zipfile.ZipFile(filename, "r") as z:
        z.extractall(config.UPLOAD_PATH)

    return jsonify(Resp(result_code=2000, result_msg="success", data=None).__dict__)


@swag_from('../swagger/post/photo/import_daily_poll_pics.yaml')
@bp_post.route('/api/post/photo/import_daily_poll_pool_pics', methods=['POST'])
def import_daily_poll_pics():
    file = request.files['file']
    ext = file.filename.split('.')[-1]
    filename = os.path.join(config.UPLOAD_PATH, 'daily_poll_pics.' + ext)
    file.save(filename)

    with zipfile.ZipFile(filename, "r") as z:
        z.extractall(config.UPLOAD_PATH)

    return jsonify(Resp(result_code=2000, result_msg="success", data=None).__dict__)


# assign poll picture
@swag_from('../swagger/post/import_poll_picture.yaml')
@bp_post.route('/api/post/import_daily_poll_assign', methods=['POST'])
def import_poll_picture():
    file = request.files['file']
    stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
    csv_input = csv.reader(stream)
    room_cleaned = []
    for key, line in enumerate(csv_input):
        if key == 0:
            if line != ['id', 'message_id', 'room_id', 'day', 'topic_no', 'photo_uri']:
                return jsonify(Resp(result_code=4000, result_msg="error content", data=None).__dict__)
            continue
        room_id = line[2]

        # clean by room_id
        if room_id not in room_cleaned:
            room = Room.query.filter_by(id=room_id).first()  # id, not room_id
            if room.activated == 1:
                return jsonify(Resp(result_code=4000, result_msg="room activated, room id: " + str(room_id),
                                data=room.serialize()).__dict__)
            messages_existed = PollPost.query.filter_by(room_id=room_id).all()
            for message in messages_existed:
                db.session.delete(message)
                db.session.commit()
            room_cleaned.append(room_id)

        topic = line[3]     # day
        message_id = line[1]
        photo_uri = line[5]

        post = PollPost(
            message_id=message_id,
            # timeline_type=config.TIMELINE_PRI,
            # post_type=1,  # fixme
            # user_id=participant.id,
            room_id=room_id,
            topic=topic,
            photo_uri=photo_uri
        )
        db.session.add(post)
        db.session.commit()

    return jsonify(Resp(result_code=2000, result_msg="success", data=None).__dict__)