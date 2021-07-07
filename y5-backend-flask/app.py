import datetime

from flasgger import Swagger
from flask import Flask, render_template, request
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_apscheduler import APScheduler
from flask_babelex import Babel
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_cors import CORS
from flask_mail import Mail
from git import Repo

import config
from blueprints.auth import bp_auth, login_manager
from blueprints.post import bp_post
from blueprints.room import bp_room
from room_socketio import RoomNamespace
from extensions import db, cache, socketio
from models import User, Room, RoomPrototype, RoomMember, Timeline, Post, PostComment, PostLike, Message, Notice, \
    PostDaily
from views import ModelViewHasMultipleImages

app = Flask(__name__)

app.config.from_object('config')
Swagger(app)
babel = Babel(app)
ckeditor = CKEditor(app)
cors = CORS(app)
mail = Mail(app)
Bootstrap(app)
cache.init_app(app)
socketio.init_app(app, engineio_logger=True)
socketio.on_namespace(RoomNamespace('/'))
login_manager.init_app(app)

admin = Admin(app=app, name=config.ADMIN_TITLE, template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session, name=u'User'))
admin.add_view(ModelView(Room, db.session, name=u'Room', category='Room'))
admin.add_view(ModelViewHasMultipleImages(Notice, db.session, name=u'Room Notice', category='Room'))
admin.add_view(ModelView(RoomPrototype, db.session, name=u'Room Prototype', category='Room'))
admin.add_view(ModelView(RoomMember, db.session, name=u'Room Member', category='Room'))
admin.add_view(ModelView(Timeline, db.session, name=u'Timeline'))
admin.add_view(ModelView(Post, db.session, name=u'Post', category='Post'))
admin.add_view(ModelView(PostDaily, db.session, name=u'Post Daily', category='Post'))
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


@app.route('/reload', methods=['POST'])
def reload():
    if request.method == 'POST':
        git_pull()
        print("reload success", str(datetime.datetime.now())[:19])
        return "reload success"


def git_pull():
    repo = Repo("./")  # git文件的路径
    git = repo.git

    print("当前未跟踪文件:", repo.untracked_files)
    print("当前本地git仓库状态:", git.status())
    print("当前本地git仓库是否有文件更新:", repo.is_dirty())
    print("当前本地分支:", git.branch())
    print("当前远程仓库:", git.remote())

    remote_name = "origin"
    print("正在 git pull {0} master".format(remote_name))
    git.pull(remote_name, "master")
    print("拉取修改 {0} 成功！".format(remote_name))


if __name__ == '__main__':
    app.run()
