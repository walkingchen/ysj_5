import os

from flask import json
from sqlalchemy import inspect

import config
from models import RoomPrototype, RoomMember, PostComment, Serializer, User, PostLike, PostFactcheck, Post, PostFlag


# 查询好友网络
def get_friends(room, user_id):
    prototype = RoomPrototype.query.filter_by(prototype_id=room.room_type).first()
    friendship = json.loads(prototype.friendship)
    member = RoomMember.query.filter_by(room_id=room.id, user_id=user_id).first()
    friend_seats = friendship[str(member.seat_no)]
    friends = RoomMember.query.filter_by(room_id=room.id).filter(RoomMember.seat_no.in_(friend_seats)).all()

    return friends


# 获取成员信息
def query_user(user_id):
    return User.query.filter(User.id == user_id) \
        .with_entities(
            User.id,
            User.nickname,
            User.realname,
            User.username,
            User.avatar,
            User.email,
            User.created_at
        ).first()


# 获取座位号
def query_membership(room_id, user_id):
    return User.query.join(RoomMember, RoomMember.user_id == User.id) \
        .filter(RoomMember.room_id == room_id, User.id == user_id) \
        .with_entities(
            User.id,
            User.nickname,
            User.realname,
            User.username,
            User.avatar,
            User.email,
            RoomMember.seat_no,
            User.created_at
        ).first()


# 为每篇post添加评论、点赞
def process_posts(posts, user_id):
    for post in posts:
        process_post(post, user_id)


def process_post(post, user_id):
    comments = PostComment.query.filter_by(post_id=post['id']).all()
    comments_serialized = []
    for comment in comments:
        comment_serialized = Serializer.serialize(comment)
        user = query_user(user_id=comment.user_id)
        comment_serialized['user'] = user._asdict()
        comments_serialized.append(comment_serialized)
    post['comments'] = comments_serialized

    likes = PostLike.query.filter(PostLike.post_id == post['id'], PostLike.post_like == 1).all()
    likes_serialized = []
    for like in likes:
        like_serialized = Serializer.serialize(like)
        user = query_user(user_id=like.user_id)
        like_serialized['user'] = user._asdict()
        likes_serialized.append(like_serialized)
    post['likes'] = {
        'count': len(likes),
        'details': likes_serialized
    }

    if post['photo_uri'] is not None:
        post['photo_uri'] = {
            'file': '/uploads/' + post['photo_uri'],
        }

        if not os.path.exists(config.UPLOAD_PATH + post['photo_uri'].split('.')[0] + '_s.jpg'):
            post['photo_uri']['small'] = '/uploads/' + post['photo_uri']
        else:
            post['photo_uri']['small'] = '/uploads/' + post['photo_uri'].split('.')[0] + '_s.jpg'

        if not os.path.exists(config.UPLOAD_PATH + post['photo_uri'].split('.')[0] + '_m.jpg'):
            post['photo_uri']['medium'] = '/uploads/' + post['photo_uri']
        else:
            post['photo_uri']['medium'] = '/uploads/' + post['photo_uri'].split('.')[0] + '_m.jpg'

    # 判断是否已点过赞
    like = PostLike.query.filter_by(post_id=post['id'], user_id=user_id, post_like=1).first()
    if like is None:
        post['liked'] = None
    else:
        post['liked'] = Serializer.serialize(like)

    dislikes = PostLike.query.filter(PostLike.post_id == post['id'], PostLike.post_like == 0).all()
    dislikes_serialized = []
    for dislike in dislikes:
        dislike_serialized = Serializer.serialize(dislike)
        user = query_user(user_id=dislike.user_id)
        dislike_serialized['user'] = user._asdict()
        dislikes_serialized.append(dislike_serialized)
    post['dislikes'] = {
        'count': len(dislikes),
        'details': dislikes_serialized
    }

    # 判断是否已点过踩
    dislike = PostLike.query.filter_by(post_id=post['id'], user_id=user_id, post_like=0).first()
    if dislike is None:
        post['disliked'] = None
    else:
        post['disliked'] = Serializer.serialize(dislike)

    # 判断是否已点过factcheck
    check = PostFactcheck.query.filter_by(post_id=post['id'], user_id=user_id).first()
    if check is not None:
        post['factcheck'] = Serializer.serialize(check)
    else:
        post['factcheck'] = None

    # 判断是否已点过flag
    flag = PostFlag.query.filter_by(post_id=post['id'], user_id=user_id).first()
    if flag is None:
        post['flagged'] = None
    else:
        post['flagged'] = Serializer.serialize(flag)

    flag_count = PostFlag.query.filter_by(post_id=post['id']).count()
    post['flags'] = {
        'count': flag_count
    }

    post_shared = Post.query.filter_by(id=post['post_shared_id']).first()
    if post_shared is not None:
        post['post_shared'] = Serializer.serialize(post_shared)
    else:
        post['post_shared'] = None


def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}