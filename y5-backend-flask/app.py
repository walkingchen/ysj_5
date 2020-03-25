from socket import SocketIO

from flasgger import Swagger
from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_apscheduler import APScheduler
from flask_babelex import Babel
from flask_bootstrap import Bootstrap
from flask_cache import Cache
from flask_ckeditor import CKEditor
from flask_cors import CORS
from flask_login import LoginManager
from flask_mail import Mail

import config
from blueprints.room import bp_room
from extensions import db
from models import User, Room, RoomPrototype, RoomMember, Timeline, Post, PostComment, PostLike, Message

app = Flask(__name__)

app.config.from_object('config')
cors = CORS(app)
mail = Mail(app)
Bootstrap(app)
Swagger(app)
babel = Babel(app)
ckeditor = CKEditor(app)
cache = Cache(config={'CACHE_TYPE': 'simple'})
cache.init_app(app)
socketio = SocketIO(app, 'rw')

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

admin = Admin(app=app, name=config.ADMIN_TITLE, template_mode='bootstrap3')
admin.add_view(ModelView(Room, db.session, name=u'Room', category='Room'))
admin.add_view(ModelView(RoomPrototype, db.session, name=u'RoomPrototype', category='Room'))
admin.add_view(ModelView(RoomMember, db.session, name=u'RoomMember', category='Room'))
admin.add_view(ModelView(Timeline, db.session, name=u'Timeline'))
admin.add_view(ModelView(Post, db.session, name=u'Post', category='Post'))
admin.add_view(ModelView(PostComment, db.session, name=u'PostComment', category='Post'))
admin.add_view(ModelView(PostLike, db.session, name=u'PostLike', category='Post'))
admin.add_view(ModelView(Message, db.session, name=u'Message', category='Chat'))

db.init_app(app)

scheduler = APScheduler()
scheduler.init_app(app)
# scheduler.start()

app.register_blueprint(bp_room)


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


if __name__ == '__main__':
    app.run()
