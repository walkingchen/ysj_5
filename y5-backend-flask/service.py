from flask import json
from sqlalchemy import inspect

from models import RoomPrototype, RoomMember, PostComment, Serializer, User, PostLike


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
        comments = PostComment.query.filter_by(post_id=post['id']).all()
        comments_serialized = []
        for comment in comments:
            comment_serialized = Serializer.serialize(comment)
            user = query_user(user_id=comment.user_id)
            comment_serialized['user'] = user._asdict()
            comments_serialized.append(comment_serialized)
        post['comments'] = comments_serialized

        likes = PostLike.query.filter_by(post_id=post['id']).all()
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

        # 判断是否已点过赞
        like = PostLike.query.filter_by(post_id=post['id'], user_id=user_id).first()
        if like is None:
            post['liked'] = False
        else:
            post['liked'] = True


def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}