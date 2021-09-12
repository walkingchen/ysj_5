# coding: utf-8
import datetime

from flask_login import UserMixin
from sqlalchemy import Column, DateTime, Integer, MetaData, String, Text, inspect
from sqlalchemy.schema import FetchedValue
from sqlalchemy.ext.declarative import declarative_base
from extensions import db


def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    return x


class Serializer(object):

    def serialize(self):
        return {c: datetime_handler(getattr(self, c)) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]


class Message(db.Model):
    __tablename__ = 'tb_message'

    id = Column(Integer, primary_key=True)
    message = Column(String(255))
    message_type = Column(Integer)
    room_id = Column(Integer)
    user_id_from = Column(Integer)
    user_id_to = Column(Integer)
    created_at = Column(DateTime, server_default=FetchedValue())
    updated_at = Column(DateTime)


class Notice(db.Model):
    __tablename__ = 'tb_notice'

    id = Column(Integer, primary_key=True)
    notice_type = Column(Integer, info='公告类型：0全局，1room')
    message = Column(Text)
    images = Column(Text)
    created_at = Column(DateTime, server_default=FetchedValue())
    updated_at = Column(DateTime)


class Post(db.Model):
    __tablename__ = 'tb_post'

    id = Column(Integer, primary_key=True)
    post_title = Column(String(256))
    post_content = Column(Text)
    post_type = Column(Integer)
    photo_uri = Column(String(128))
    keywords = Column(String(256))
    abstract = Column(Text)
    user_id = Column(Integer)
    topic = Column(Integer)
    timeline_type = Column(Integer)
    room_id = Column(Integer)
    post_shared_id = db.Column(db.Integer)
    created_at = Column(DateTime, server_default=FetchedValue())
    updated_at = Column(DateTime)

    def serialize(self):
        d = Serializer.serialize(self)
        return d


class PrivateMessage(db.Model):
    __tablename__ = 'tb_private_message'

    id = Column(Integer, primary_key=True)
    message_id = Column(Integer)
    message_title = Column(String(256))
    message_content = Column(Text)
    photo_uri = Column(String(128))
    keywords = Column(String(256))
    abstract = Column(Text)
    updated_at = Column(DateTime, nullable=False, server_default=FetchedValue())
    created_at = Column(DateTime, server_default=FetchedValue())


class Photo(db.Model):
    __tablename__ = 'tb_post_photo'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(500))
    filename = db.Column(db.String(64))
    filename_s = db.Column(db.String(64))
    filename_m = db.Column(db.String(64))
    author_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.FetchedValue())


class PostStatus(db.Model):
    __tablename__ = 'tb_post_status'

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    read_status = db.Column(db.Integer, server_default=db.FetchedValue())
    created_at = db.Column(db.DateTime, server_default=db.FetchedValue())
    updated_at = db.Column(db.DateTime, server_default=db.FetchedValue())


class PostDaily(db.Model):
    __tablename__ = 'tb_post_daily'

    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer)
    post_id = db.Column(db.Integer)
    topic = db.Column(db.Integer)
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    created_at = db.Column(db.DateTime, server_default=db.FetchedValue())


class PostComment(db.Model):
    __tablename__ = 'tb_post_comment'

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer)
    user_id = Column(Integer)
    comment_content = Column(String(140))
    created_at = Column(DateTime, server_default=FetchedValue())
    updated_at = Column(DateTime)

    def serialize(self):
        d = Serializer.serialize(self)
        return d


class CommentFlag(db.Model):
    __tablename__ = 'tb_comment_flag'

    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    flag = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.FetchedValue())
    updated_at = db.Column(db.DateTime, server_default=db.FetchedValue())

    def serialize(self):
        d = Serializer.serialize(self)
        return d


class CommentLike(db.Model):
    __tablename__ = 'tb_comment_like'

    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    comment_like = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.FetchedValue())
    updated_at = db.Column(db.DateTime, server_default=db.FetchedValue())

    def serialize(self):
        d = Serializer.serialize(self)
        return d


class CommentStatus(db.Model):
    __tablename__ = 'tb_comment_status'

    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    read_status = db.Column(db.Integer, server_default=db.FetchedValue())
    created_at = db.Column(db.DateTime, server_default=db.FetchedValue())
    updated_at = db.Column(db.DateTime, server_default=db.FetchedValue())


class Redspot(db.Model):
    __tablename__ = 'tb_redspot'

    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    topic = db.Column(db.Integer)
    unread = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.FetchedValue())
    updated_at = db.Column(db.DateTime, server_default=db.FetchedValue())

    def serialize(self):
        d = Serializer.serialize(self)
        return d


class PostLike(db.Model):
    __tablename__ = 'tb_post_like'

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer)
    user_id = Column(Integer)
    post_like = Column(Integer, info='1: like; 0: dislike')
    created_at = Column(DateTime, server_default=FetchedValue())
    updated_at = Column(DateTime, server_default=FetchedValue())

    def serialize(self):
        d = Serializer.serialize(self)
        return d


class PostFlag(db.Model):
    __tablename__ = 'tb_post_flag'

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    flag = db.Column(db.Integer, server_default=db.FetchedValue())
    created_at = db.Column(db.DateTime, server_default=db.FetchedValue())
    updated_at = db.Column(db.DateTime, server_default=db.FetchedValue())


class PostFactcheck(db.Model):
    __tablename__ = 'tb_post_factcheck'

    id = Column(Integer, primary_key=True)
    room_id = Column(Integer)
    post_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=FetchedValue())


class PostType(db.Model):
    __tablename__ = 'tb_post_type'

    id = Column(Integer, primary_key=True)
    type_name = Column(String(64), nullable=False)
    type_structure = Column(String(2048))
    created_at = Column(DateTime, server_default=FetchedValue())
    updated_at = Column(DateTime, server_default=FetchedValue())


class Question(db.Model):
    __tablename__ = 'tb_question'

    id = Column(Integer, primary_key=True)


class Room(db.Model):
    __tablename__ = 'tb_room'

    id = Column(Integer, primary_key=True)
    room_id = Column(String(255))
    room_name = Column(String(255))
    room_desc = Column(String(255))
    room_type = Column(Integer)
    people_limit = Column(Integer)
    activated = Column(Integer, server_default=FetchedValue())
    created_at = Column(DateTime, server_default=FetchedValue())
    updated_at = Column(DateTime)

    def serialize(self):
        d = Serializer.serialize(self)
        return d


class RoomMember(db.Model):
    __tablename__ = 'tb_room_member'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    seat_no = Column(Integer)
    room_id = Column(Integer)
    activated = Column(Integer, server_default=FetchedValue())
    created_at = Column(DateTime, server_default=FetchedValue())
    updated_at = Column(DateTime)

    def serialize(self):
        d = Serializer.serialize(self)
        return d


class RoomPrototype(db.Model):
    __tablename__ = 'tb_room_prototype'

    id = Column(Integer, primary_key=True)
    prototype_id = Column(Integer)
    prototype_name = Column(String(128))
    people_limit = Column(Integer)
    friendship = Column(String)
    created_at = Column(DateTime, server_default=FetchedValue())
    updated_at = Column(DateTime, server_default=FetchedValue())

    def serialize(self):
        d = Serializer.serialize(self)
        return d


class Timeline(db.Model):
    __tablename__ = 'tb_timeline'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    room_id = Column(Integer)
    timeline_type = Column(Integer, info='公共0/私人1')
    created_at = Column(DateTime, server_default=FetchedValue())
    updated_at = Column(DateTime)


class User(db.Model, UserMixin):
    __tablename__ = 'tb_user'

    id = Column(Integer, primary_key=True)
    # user_id = Column(Integer)
    username = Column(String(32))
    password = Column(String(128))
    email = Column(String(128))
    nickname = Column(String(32))
    realname = Column(String(32))
    avatar = Column(String(2048))
    created_at = Column(DateTime, server_default=FetchedValue())
    updated_at = Column(DateTime)


class UserProfile(db.Model):
    __tablename__ = 'tb_user_profile'

    user_id = Column(Integer, primary_key=True)
    user_status = Column(Integer)
    created_at = Column(DateTime, server_default=FetchedValue())
    updated_at = Column(DateTime)
