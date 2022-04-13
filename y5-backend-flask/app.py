import datetime
import os
import time

from flasgger import Swagger
from flask import Flask, render_template, request, jsonify
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_apscheduler import APScheduler
from flask_babelex import Babel
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_cors import CORS
from flask_login import current_user
from flask_mail import Mail, Message
from git import Repo

import config
from blueprints.auth import bp_auth, login_manager
from blueprints.mail import bp_mail
from blueprints.post import bp_post
from blueprints.room import bp_room
from blueprints.user import bp_user
from entity.Resp import Resp
from room_socketio import RoomNamespace
from extensions import db, cache, socketio, scheduler, mail
from models import User, Room, RoomPrototype, RoomMember, Timeline, PublicPost, PostComment, PostLike, \
    SystemMessage, PrivateMessage, PostFlag, PrivatePost, SystemPost, PollPost, CommentStatus, PostStatus, MailTemplate

app = Flask(__name__)

app.config.from_object('config')
Swagger(app)
babel = Babel(app)
ckeditor = CKEditor(app)
cors = CORS(app)
mail.init_app(app)
Bootstrap(app)
cache.init_app(app)
socketio.init_app(app, engineio_logger=True)
socketio.on_namespace(RoomNamespace('/'))
login_manager.init_app(app)


db.init_app(app)

scheduler.init_app(app)
scheduler.start()


from views import RoomModelView, PostModelView, YModelView, UserModelView, RoomMemberModelView, PublicPostModelView

admin = Admin(app=app, name=config.ADMIN_TITLE, template_mode='bootstrap3')
admin.add_view(UserModelView(User, db.session, name=u'User'))

admin.add_view(RoomModelView(Room, db.session, name=u'Room', category='Room'))
admin.add_view(ModelView(RoomPrototype, db.session, name=u'Room Prototype', category='Room'))
admin.add_view(RoomMemberModelView(RoomMember, db.session, name=u'Room Member', category='Room'))

# admin.add_view(PostModelView(PrivatePost, db.session, name=u'Private Post', category='Post'))
admin.add_view(PublicPostModelView(PublicPost, db.session, name=u'Public Post', category='Post'))
admin.add_view(YModelView(PostComment, db.session, name=u'Post Comment', category='Post'))
admin.add_view(YModelView(PostFlag, db.session, name=u'Post Flag', category='Post'))
admin.add_view(YModelView(PostLike, db.session, name=u'Post Like', category='Post'))

admin.add_view(YModelView(PrivateMessage, db.session, name=u'Private Message Pool', category='Private Message'))
admin.add_view(PostModelView(PrivatePost, db.session, name=u'Private Message Assign', category='Private Message'))

admin.add_view(YModelView(SystemMessage, db.session, name=u'System Message Pool', category='System Message'))
# move system post into public post with is_system_post=1
# admin.add_view(YModelView(SystemPost, db.session, name=u'System Message Assign', category='System Message'))

admin.add_view(YModelView(PollPost, db.session, name=u'Daily Poll Assign', category='Daily Poll'))


app.register_blueprint(bp_room)
app.register_blueprint(bp_post)
app.register_blueprint(bp_auth)
app.register_blueprint(bp_user)
app.register_blueprint(bp_mail)


@app.route('/chat', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/mail')
def test_mail():
    mail_night()

    return render_template('404.html')


def reload_vue():
    os.system('cd ' + config.BASE_DIR + '/frontend')
    os.system('yarn build')
    os.system('sudo rm /var/www/ysj_5_frontend -rf')
    os.system('sudo mv dist /var/www/')
    os.system('sudo chown www-data:www-data /var/www/ysj_5_frontend')
    os.system('cd ' + config.PROJECT_ROOT)


@app.route('/reload', methods=['POST'])
def reload():
    if request.method == 'POST':
        # json = request.args()

        # if json['sender']['login'] == 'codingchan':
        git_pull()
        
        print("reload success", str(datetime.datetime.now())[:19])
        return "reload success"


def git_pull():
    repo = Repo(config.BASE_DIR)
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


# @scheduler.task('cron', id='job_mail_morning', day='*', hour='8', minute='0', second='0')
def mail_morning():
    with app.app_context():
        message = 'mail_morning'
        subject = "mail_morning"
        rooms = Room.query.filter_by(activated=1).all()
        for room in rooms:
            day_activated = room.activated_at
            # day = today - day_activated
            day = 8
            room_members = RoomMember.query.filter_by(room_id=room.id).all()
            for member in room_members:
                user = User.query.filter_by(id=member.user_id).first()
                if user.email is not None:
                    msg = Message(recipients=['cenux1987@163.com'],
                                  body=message,
                                  subject=subject,
                                  sender=("Admin", "sijia.yang@alumni.upenn.edu"))

                    mail.send(msg)


# @scheduler.task('cron', id='job_mail_night', day='*', hour='20', minute='0', second='0')
def mail_night():
    with app.app_context():
        today = datetime.datetime.today().date()
        tomorrow = datetime.datetime.today().date() + datetime.timedelta(days=1)

        # room activate day
        rooms = Room.query.filter_by(activated=1).all()
        for room in rooms:
            day_activated = room.activated_at
            day = today - day_activated.date()
            day = day.days
            # day = 8
            room_members = RoomMember.query.filter_by(room_id=room.id).all()
            member_ids = []
            for member in room_members:
                member_ids.append(member.user_id)

            # room level
            new_post_count = PublicPost.query.filter_by(room_id=room.id).filter_by(topic=day).count()

            # comments
            new_comment_count = PostComment.query.filter(PostComment.user_id.in_(tuple(member_ids))).filter(
                PostComment.created_at >= today,
                PostComment.created_at < tomorrow
            ).count()

            # likes
            new_like_count = PostLike.query.filter(PostLike.user_id.in_(tuple(member_ids))).filter(
                PostLike.created_at >= today,
                PostLike.created_at < tomorrow
            ).count()

            # flags
            new_flag_count = PostFlag.query.filter(PostFlag.user_id.in_(tuple(member_ids))).filter(
                PostFlag.created_at >= today,
                PostFlag.created_at < tomorrow
            ).count()

            # user level
            for member in room_members:
                private_posts = PrivatePost.query.filter_by(user_id=member.id).filter_by(
                    room_id=room.id).filter_by(topic=day).all()
                # titles
                titles = ''
                for post in private_posts:
                    titles += post.post_title
                    titles += ', '

                message_template = MailTemplate.query.filter_by(mail_type=2).first()    # type=2: night mail template
                message = message_template.content % (titles, new_post_count, new_comment_count, new_like_count, new_flag_count)

                subject = message_template.title
                user = User.query.filter_by(id=member.user_id).first()
                if user.email is not None:
                    msg = Message(recipients=[user.email],
                                  body=message,
                                  subject=subject,
                                  sender=("Admin", "sijia.yang@alumni.upenn.edu"))
                    msg.html = message

                    mail.send(msg)


with app.app_context():
    mail_template_morning = MailTemplate.query.filter_by(mail_type=1).first()
    scheduler.add_job(func=mail_morning, trigger='cron', hour=mail_template_morning.send_hour, id='job_mail_morning')

    mail_template_night = MailTemplate.query.filter_by(mail_type=2).first()
    scheduler.add_job(func=mail_night, trigger='cron', hour=mail_template_night.send_hour, id='job_mail_night')


if __name__ == '__main__':
    app.run()