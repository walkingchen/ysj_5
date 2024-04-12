import datetime
import logging
import os
import time

from flasgger import Swagger
from flask import Flask, render_template, request
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_babelex import Babel
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_cors import CORS
from flask_mail import Message
from git import Repo
from sqlalchemy import desc

import config
from blueprints.auth import bp_auth, login_manager
from blueprints.mail import bp_mail
from blueprints.post import bp_post
from blueprints.room import bp_room
from blueprints.user import bp_user
from room_socketio import RoomNamespace
from extensions import db, cache, socketio, scheduler, mail
from models import User, Room, RoomPrototype, RoomMember, PublicPost, PostComment, PostLike, \
    SystemMessage, PrivateMessage, PostFlag, PrivatePost, PollPost, MailTemplate

app = Flask(__name__)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logging.basicConfig()

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


@app.route('/test_mail_morning')
# @scheduler.task('cron', id='job_mail_morning', day='*', hour='8', minute='0', second='0')
def mail_morning():
    with app.app_context():
        subject = 'mail_morning'

        rooms = Room.query.filter_by(activated=1).all()
        for room in rooms:
            # get topics
            room = Room.query.get(room.id)
            activated_at = room.activated_at
            if activated_at is None:
                continue
            local_time = time.localtime(int(activated_at.timestamp()))
            activated_day = local_time.tm_yday
            activated_year = local_time.tm_year
            print('activated_day = ' + str(activated_day))

            now = time.localtime(time.time())
            now_day = now.tm_yday
            now_year = now.tm_year
            print('now_day = ' + str(now_day))

            if now_year > activated_year:
                n = now_day + 365 - activated_day + 1
            else:
                n = now_day - activated_day + 1

            if n > 8:
                continue

            # 输出room.id、day
            print('room.id = ' + str(room.id) + ' day = ' + str(n))
            mail_template_morning = MailTemplate.query.filter_by(room_id=room.id).filter_by(day=n).filter_by(mail_type=1).first()
            # if mail_template_morning is None:
            #     return

            message_html = '''
                <!DOCTYPE html>
                <html lang="en">
                <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Notification</title>
                <style>
                  body {
                    font-family: Arial, sans-serif;
                    background-color: #f2f2f2;
                    padding: 15px;
                  }
                  .container {
                    background-color: #f9f9f9;
                    border-radius: 10px;
                    padding: 10px;
                    margin: 10px;
                  }
                  strong {
                    font-weight: bold;
                  }
                  .title {
                    font-weight: bold;
                    font-size: 16px;
                    margin-bottom: 10px;
                  }
                  .login-button {
                    background-color: #007bff;
                    color: white;
                    padding: 15px;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                  }
                  .login-button:hover {
                    background-color: #0056b3;
                  }
                </style>
                </head>
                <body>
                <div class="container">
                    %s
                </div>
                <div>
                  <img src="%s" alt="">
                </div>
                <div style="margin: 30px 15px;">
                  <a class="login-button" href="https://camer-covid.journalism.wisc.edu/">Click to login back</a>
                </div>
                </body>
                </html>
            '''

            message = PollPost.query.filter_by(
                room_id=room.id,
                topic=n
            ).first()

            if message is not None:
                photo_uri = 'http://ysj_5.soulfar.com/uploads/' + message.photo_uri
            else:
                photo_uri = 'http://ysj_5.soulfar.com/uploads/daily_poll.jpeg'

            img_str = photo_uri

            message = message_html % (mail_template_morning.content, img_str)
            room_members = RoomMember.query.filter_by(room_id=room.id).all()
            for member in room_members:
                subject = mail_template_morning.title
                user = User.query.filter_by(id=member.user_id).first()
                if user.email is not None:
                    msg = Message(recipients=[user.email],
                    # msg = Message(recipients=['cenux1987@163.com'],
                                  body=message,
                                  subject=subject,
                                  sender=("Admin", "sijia.yang@alumni.upenn.edu"))
                    msg.html = message
                    mail.send(msg)


# @scheduler.task('cron', id='job_mail_night', day='*', hour='20', minute='0', second='0')
@app.route('/test_mail', methods=['GET'])
def mail_night():
    with app.app_context():
        today = datetime.datetime.today().date()
        tomorrow = datetime.datetime.today().date() + datetime.timedelta(days=1)

        # room activate day
        rooms = Room.query.filter_by(activated=1).all()
        for room in rooms:
            day_activated = room.activated_at
            # FIXME 解决本地时间和服务器时间不一致问题
            day = today - day_activated.date()
            day = day.days
            print('day = ' + str(day))
            if day > 8:
                return
            room_members = RoomMember.query.filter_by(room_id=room.id).all()
            member_ids = []
            post_str = ""
            for member in room_members:
                member_ids.append(member.user_id)

            public_post_count = PublicPost.query.filter_by(
                room_id=room.id,
                topic=day,
                is_system_post=0
            ).filter_by().count()
            public_posts = PublicPost.query.filter_by(
                room_id=room.id,
                topic=day,
                is_system_post=0
            ).order_by(desc(PublicPost.created_at)).limit(5).all()

            post_str = '''<div class="container">'''
            if public_post_count > 0:
                post_str += '<p class="title">New post count: %d</p>' % public_post_count
                for post in public_posts:
                    user = User.query.filter_by(id=post.user_id).first()
                    post_words = post.post_content.split()
                    print(post_words[:10])
                    post_str += "<p>" + user.nickname + ": " + ' '.join(post_words[:10]) + "......</p>"

            system_post_count = PublicPost.query.filter_by(
                room_id=room.id,
                topic=day,
                is_system_post=1
            ).filter_by().count()
            system_posts = PublicPost.query.filter_by(
                room_id=room.id,
                topic=day,
                is_system_post=1
            ).order_by(desc(PublicPost.created_at)).limit(1).all()
            if system_post_count > 0:
                for post in system_posts:
                    post_words = post.abstract.split()
                    print(post_words[:10])
                    post_str += "<p>COVID Flashbacks: " + ' '.join(post_words[:10]) + "......</p>"
            post_str += "</div>"

            # comments
            new_comments = PostComment.query.filter(PostComment.user_id.in_(tuple(member_ids))).filter(
                PostComment.created_at >= today,
                PostComment.created_at < tomorrow
            ).all()
            comment_str = ""
            if len(new_comments) > 0:
                comment_str = '''<div class="container">'''
                comment_str += '<p class="title">New comments: %d</p>' % len(new_comments)
                for comment in new_comments:
                    user = User.query.filter_by(id=comment.user_id).first()
                    comment_words = comment.split()
                    comment_str += "<p>" + user.nickname + ": " + ' '.join(comment_words[:10]) + "......</p>"
                comment_str += "</div>"

            # likes
            new_likes = PostLike.query.filter(PostLike.user_id.in_(tuple(member_ids))).filter(
                PostLike.created_at >= today,
                PostLike.created_at < tomorrow
            ).all()
            like_str = ""
            if len(new_likes) > 0:
                like_str = '''<div class="container">'''
                like_str += '<p class="title">New likes: %d</p>' % len(new_likes)
                for like in new_likes:
                    user = User.query.filter_by(id=like.user_id).first()
                    post = PublicPost.query.filter_by(id=like.post_id).first()
                    post_author = User.query.filter_by(id=post.user_id).first()
                    like_str += "<p>" + user.nickname + " likes " + post_author.nickname + "'s post.</p>"
                like_str += "</div>"

            # # flags
            # new_flag_count = PostFlag.query.filter(PostFlag.user_id.in_(tuple(member_ids))).filter(
            #     PostFlag.created_at >= today,
            #     PostFlag.created_at < tomorrow
            # ).count()

            message_html = '''
                <!DOCTYPE html>
                <html lang="en">
                <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Notification</title>
                <style>
                  body {
                    font-family: Arial, sans-serif;
                    background-color: #f2f2f2;
                    padding: 15px;
                  }
                  .container {
                    background-color: #f9f9f9;
                    border-radius: 10px;
                    padding: 10px;
                    margin: 10px;
                  }
                  strong {
                    font-weight: bold;
                  }
                  .title {
                    font-weight: bold;
                    font-size: 16px;
                    margin-bottom: 10px;
                  }
                  .login-button {
                    background-color: #007bff;
                    color: white;
                    padding: 15px;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                  }
                  .login-button:hover {
                    background-color: #0056b3;
                  }
                </style>
                </head>
                <body>
                <div class="container">
                  %s
                </div>
                <!-- posts -->
                  %s
                <!-- comments -->
                  %s
                <!-- likes -->
                  %s
                <div style="margin: 30px 15px;">
                  <a class="login-button" href="https://camer-covid.journalism.wisc.edu/">Click to login back</a>
                </div>
                </body>
                </html>
            '''
            for member in room_members:
                # 根据早晚类型及天数获取邮件模板
                message_template = MailTemplate.query.filter_by(room_id=room.id, mail_type=2,
                                                                day=day).first()  # type=2: night mail template
                if message_template is None:
                    print("No mail template for room %d" % room.id)
                    continue
                message = message_html % (message_template.content, post_str, comment_str, like_str)

                subject = message_template.title
                user = User.query.filter_by(id=member.user_id).first()
                if user.email is not None:
                    msg = Message(recipients=[user.email],
                    # msg = Message(recipients=['cenux1987@163.com'],
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
    app.run(host='0.0.0.0', debug=True)
