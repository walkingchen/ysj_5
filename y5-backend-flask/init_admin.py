from flask_admin.contrib.sqla import ModelView

from extensions import db
from models import User, Room, RoomPrototype, RoomMember, Timeline, Post, PostComment, PostLike, Message, Notice, \
    PostDaily, PrivateMessage, PostFlag
from views import ModelViewHasMultipleImages, RoomModelView, PostModelView


def init_admin(admin):
    admin.add_view(ModelView(User, db.session, name=u'User'))
    admin.add_view(RoomModelView(Room, db.session, name=u'Room', category='Room'))
    admin.add_view(ModelViewHasMultipleImages(Notice, db.session, name=u'Room Notice', category='Room'))
    admin.add_view(ModelView(RoomPrototype, db.session, name=u'Room Prototype', category='Room'))
    admin.add_view(ModelView(RoomMember, db.session, name=u'Room Member', category='Room'))
    # admin.add_view(ModelView(Timeline, db.session, name=u'Timeline'))
    admin.add_view(PostModelView(Post, db.session, name=u'Post', category='Post'))
    admin.add_view(ModelView(PostComment, db.session, name=u'Post Comment', category='Post'))
    admin.add_view(ModelView(PostFlag, db.session, name=u'Post Flag', category='Post'))
    admin.add_view(ModelView(PostLike, db.session, name=u'Post Like', category='Post'))
    admin.add_view(ModelView(PrivateMessage, db.session, name=u'PrivateMessage'))
    admin.add_view(ModelView(PostDaily, db.session, name=u'Post Daily'))
    # admin.add_view(ModelView(Message, db.session, name=u'Message', category='Chat'))