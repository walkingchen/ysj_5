from flasgger import Swagger
from flask import Flask, render_template
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
from flask_socketio import SocketIO

import config
from blueprints.auth import bp_auth
from blueprints.post import bp_post
from blueprints.room import bp_room
from chat import ChatRoomNamespace
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
socketio = SocketIO()
socketio.on_namespace(ChatRoomNamespace('/'))
socketio.init_app(app, engineio_logger=False)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

admin = Admin(app=app, name=config.ADMIN_TITLE, template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session, name=u'User'))
admin.add_view(ModelView(Room, db.session, name=u'Room', category='Room'))
admin.add_view(ModelView(RoomPrototype, db.session, name=u'Room Prototype', category='Room'))
admin.add_view(ModelView(RoomMember, db.session, name=u'Room Member', category='Room'))
admin.add_view(ModelView(Timeline, db.session, name=u'Timeline'))
admin.add_view(ModelView(Post, db.session, name=u'Post', category='Post'))
admin.add_view(ModelView(PostComment, db.session, name=u'Post Comment', category='Post'))
admin.add_view(ModelView(PostLike, db.session, name=u'Post Like', category='Post'))
admin.add_view(ModelView(Message, db.session, name=u'Message', category='Chat'))

db.init_app(app)

scheduler = APScheduler()
scheduler.init_app(app)
# scheduler.start()

app.register_blueprint(bp_room)
app.register_blueprint(bp_post)
app.register_blueprint(bp_auth)


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


@app.route('/chat', methods=['GET'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
