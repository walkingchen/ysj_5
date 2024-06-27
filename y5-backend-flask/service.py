import csv
import logging
import os

from flask import json
from sqlalchemy import inspect, func

import config
from extensions import db
from models import RoomPrototype, RoomMember, PostComment, Serializer, User, PostLike, PostFactcheck, PublicPost, \
    PostFlag, \
    PostStatus, CommentStatus, CommentFlag, CommentLike, Room, PrivateMessage, PrivatePost


# 查询好友网络
def get_friends(room, user_id):
    prototype = RoomPrototype.query.filter_by(prototype_id=room.room_type).first()
    friendship = json.loads(prototype.friendship)
    member = RoomMember.query.filter_by(room_id=room.id, user_id=user_id).first()
    # FIXME
    logging.info("room id = %d" % room.id)
    logging.info("user id = %d" % user_id)

    friend_seats = friendship[str(member.seat_no)]
    friends = RoomMember.query.filter_by(room_id=room.id).filter(RoomMember.seat_no.in_(friend_seats)).all()

    return friends


# 获取成员信息
def query_user(user_id):
    return User.query.filter(User.id == user_id) \
        .with_entities(
            User.id,
            User.nickname,
            # User.realname,
            # User.username,
            User.avatar,
            User.email,
            User.created_at
        ).first()


# 获取座位号
def query_membership(room_id, user_id):
    return User.query.join(RoomMember, RoomMember.user_id == User.id) \
        .filter(RoomMember.room_id == room_id, User.id == user_id, RoomMember.activated == 1) \
        .with_entities(
            User.id,
            User.nickname,
            # User.realname,
            # User.username,
            User.avatar,
            User.email,
            RoomMember.seat_no,
            User.created_at
        ).first()


# 为每篇post添加评论、点赞
def process_posts(posts, user_id):
    for post in posts:
        process_post(post, user_id)


def process_photo(post):
    if post['photo_uri'] is not None:
        tmp = post['photo_uri']

        post['photo_uri'] = {
            'file': '/uploads/' + tmp,
        }

        if not os.path.exists(config.UPLOAD_PATH + tmp.split('.')[0] + '_s.jpg'):
            post['photo_uri']['small'] = '/uploads/' + tmp
        else:
            post['photo_uri']['small'] = '/uploads/' + tmp.split('.')[0] + '_s.jpg'

        if not os.path.exists(config.UPLOAD_PATH + tmp.split('.')[0] + '_m.jpg'):
            post['photo_uri']['medium'] = '/uploads/' + tmp
        else:
            post['photo_uri']['medium'] = '/uploads/' + tmp.split('.')[0] + '_m.jpg'


def process_post(post, user_id):
    author = query_user(user_id=post['user_id'])
    post['user'] = author._asdict()
    post['comments_all_read'] = True
    comments = PostComment.query.filter_by(post_id=post['id']).order_by(PostComment.created_at.asc()).all()
    comments_serialized = []
    for comment in comments:
        comment_serialized = Serializer.serialize(comment)
        user = query_user(user_id=comment.user_id)
        comment_serialized['user'] = user._asdict()

        # check read status
        comment_status = CommentStatus.query.filter_by(comment_id=comment_serialized['id'], user_id=user_id).first()
        if comment_status is None:
            comment_serialized['read_status'] = False    # unread
            post['comments_all_read'] = False
            comment_status = CommentStatus(comment_id=comment_serialized['id'], user_id=user_id, read_status=1)
            db.session.add(comment_status)
            db.session.commit()
        else:
            comment_serialized['read_status'] = True    # read
        comment_flag_count = CommentFlag.query.filter_by(comment_id=comment_serialized['id']).count()
        comment_serialized['flags'] = {
            'count': comment_flag_count
        }
        comment_flag = CommentFlag.query.filter_by(comment_id=comment_serialized['id'], user_id=user_id).first()
        if comment_flag is not None:
            comment_serialized['flagged'] = Serializer.serialize(comment_flag)
        else:
            comment_serialized['flagged'] = None

        comment_like_count = CommentLike.query.filter_by(comment_id=comment_serialized['id']).count()
        comment_serialized['likes'] = {
            'count': comment_like_count
        }
        comment_like = CommentLike.query.filter_by(comment_id=comment_serialized['id'], user_id=user_id).first()
        if comment_like is not None:
            comment_serialized['liked'] = Serializer.serialize(comment_like)
        else:
            comment_serialized['liked'] = None

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

    process_photo(post)

    # 判断是否已点过赞
    like = PostLike.query.filter_by(post_id=post['id'], user_id=user_id, post_like=1).first()
    if like is None:
        post['liked'] = None
    else:
        post['liked'] = Serializer.serialize(like)

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

    post_shared = PrivatePost.query.filter_by(id=post['post_shared_id']).first()
    if post_shared is not None:
        process_post_serialized = Serializer.serialize(post_shared)
        process_post(process_post_serialized, user_id)
        post['post_shared'] = process_post_serialized
    else:
        post['post_shared'] = None

    post_status = PostStatus.query.filter_by(post_id=post['id'], user_id=user_id).first()
    if post_status is None:
        post['read_status'] = False   # unread
        post_status = PostStatus(post_id=post['id'], user_id=user_id, read_status=1)
        db.session.add(post_status)
        db.session.commit()
    else:
        post['read_status'] = True   # read


def get_top_participants(room_id):
    # 获取每个参与者在指定房间的发帖数量
    post_counts = db.session.query(
        PublicPost.room_id.label('room_id'),
        func.date(PublicPost.created_at).label('date'),
        PublicPost.user_id.label('user_id'),
        func.count(PublicPost.id).label('post_count')
    ).filter(
        PublicPost.room_id == room_id
    ).group_by(
        PublicPost.room_id,
        func.date(PublicPost.created_at),
        PublicPost.user_id
    ).subquery()

    # 获取每个参与者在指定房间的评论数量
    comment_counts = db.session.query(
        PublicPost.room_id.label('room_id'),
        func.date(PostComment.created_at).label('date'),
        PostComment.user_id.label('user_id'),
        func.count(PostComment.id).label('comment_count')
    ).join( # Join with PublicPost to get room_id
        PublicPost, PostComment.post_id == PublicPost.id
    ).filter(
        PublicPost.room_id == room_id
    ).group_by(
        PublicPost.room_id,
        func.date(PostComment.created_at),
        PostComment.user_id
    ).subquery()

    # 合并帖子和评论数量
    merged_counts = db.session.query(
        post_counts.c.room_id.label('room_id'),
        post_counts.c.date.label('date'),
        post_counts.c.user_id.label('user_id'),
        (post_counts.c.post_count + func.coalesce(comment_counts.c.comment_count, 0)).label('total_count')
    ).outerjoin(
        comment_counts,
        (post_counts.c.room_id == comment_counts.c.room_id) &
        (post_counts.c.date == comment_counts.c.date) &
        (post_counts.c.user_id == comment_counts.c.user_id)
    ).union_all(
        db.session.query(
            comment_counts.c.room_id.label('room_id'),
            comment_counts.c.date.label('date'),
            comment_counts.c.user_id.label('user_id'),
            comment_counts.c.comment_count.label('total_count')
        ).outerjoin(
            post_counts,
            (comment_counts.c.room_id == post_counts.c.room_id) &
            (comment_counts.c.date == post_counts.c.date) &
            (comment_counts.c.user_id == post_counts.c.user_id)
        ).filter(post_counts.c.user_id == None)
    ).subquery()

    # 获取指定房间每天发帖和评论数量最多的前两位参与者
    result = db.session.query(
        merged_counts.c.room_id,
        merged_counts.c.date,
        merged_counts.c.user_id,
        merged_counts.c.total_count
    ).order_by(
        merged_counts.c.room_id,
        merged_counts.c.date,
        merged_counts.c.total_count.desc()
    ).all()

    # 处理结果，获取前两位参与者
    from collections import defaultdict

    top_n_results = defaultdict(list)
    n = 2

    for row in result:
        key = (row.room_id, row.date)
        if len(top_n_results[key]) < n:
            top_n_results[key].append({
                'user_id': row.user_id,
                'total_count': row.total_count
            })

    return top_n_results


def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}