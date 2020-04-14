from flasgger import Swagger
from flask import Flask, render_template
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_apscheduler import APScheduler
from flask_babelex import Babel
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_cors import CORS
from flask_mail import Mail

import config
from blueprints.auth import bp_auth, login_manager
from blueprints.post import bp_post
from blueprints.room import bp_room
from room_socketio import RoomNamespace
from extensions import db, cache, socketio
from models import User, Room, RoomPrototype, RoomMember, Timeline, Post, PostComment, PostLike, Message

app = Flask(__name__)

app.config.from_object('config')
Swagger(app)
babel = Babel(app)
ckeditor = CKEditor(app)
cors = CORS(app)
mail = Mail(app)
Bootstrap(app)
cache.init_app(app)
socketio.on_namespace(RoomNamespace('/'))
socketio.init_app(app, engineio_logger=False)
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


@app.route('/chat', methods=['GET'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
