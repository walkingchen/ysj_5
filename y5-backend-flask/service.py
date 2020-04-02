from flask import json
from sqlalchemy import inspect

from models import RoomPrototype, RoomMember, PostComment, Serializer, User, PostLike


def get_friends(room, user_id):
    prototype = RoomPrototype.query.filter_by(prototype_id=room.room_type).first()
    friendship = json.loads(prototype.friendship)
    member = RoomMember.query.filter_by(room_id=room.id, user_id=user_id).first()
    friend_seats = friendship[str(member.seat_no)]
    friends = RoomMember.query.filter_by(room_id=room.id).filter(RoomMember.seat_no.in_(friend_seats)).all()

    return friends


def query_membership(room_id, user_id):
    return User.query.join(RoomMember, RoomMember.user_id == User.id) \
        .filter(RoomMember.room_id == room_id, User.id == user_id) \
        .with_entities(
            User.id, User.realname, User.username, User.avatar, User.email, RoomMember.seat_no, User.created_at
        ).first()


# 为每篇post添加评论、点赞
def process_posts(posts, user_id):
    for post in posts:
        comments = PostComment.query.filter_by(post_id=post['id']).all()
        comments_serialized = Serializer.serialize_list(comments)
        for comment in comments_serialized:
            user = User.query.filter_by(id=comment['user_id'])\
                .with_entities(User.id, User.realname, User.username, User.avatar, User.email, User.created_at).first()
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


def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}