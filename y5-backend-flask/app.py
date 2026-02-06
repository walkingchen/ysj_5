import datetime
import logging
import os
import sys
import time
from logging.handlers import RotatingFileHandler

import pytz
from flasgger import Swagger
from flask import Flask, render_template, request, jsonify
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
from blueprints.payment import bp_payment, calculate_func
from blueprints.post import bp_post
from blueprints.room import bp_room
from blueprints.user import bp_user
from entity.Resp import Resp
from room_socketio import RoomNamespace
from extensions import db, cache, socketio, scheduler, mail
from models import User, Room, RoomPrototype, RoomMember, PublicPost, PostComment, PostLike, \
    SystemMessage, PrivateMessage, PostFlag, PrivatePost, PollPost, MailTemplate, Serializer
from service import get_top_participants

app = Flask(__name__)

# 配置日志系统
def setup_logging(app):
    """配置应用日志系统"""
    # 创建logs目录
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # 设置日志格式
    log_format = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s (%(filename)s:%(lineno)d): %(message)s'
    )
    
    # 文件处理器 - 记录所有日志
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, 'app.log'),
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=10
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(log_format)
    
    # 错误日志文件处理器
    error_file_handler = RotatingFileHandler(
        os.path.join(log_dir, 'error.log'),
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=10
    )
    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(log_format)
    
    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(log_format)
    
    # 配置应用logger
    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.addHandler(error_file_handler)
    app.logger.addHandler(console_handler)
    
    # 配置根logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(error_file_handler)
    root_logger.addHandler(console_handler)
    
    return app.logger

logger = setup_logging(app)

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

from views import (RoomModelView, PostModelView, YModelView, UserModelView, 
                   RoomMemberModelView, PublicPostModelView, DataExportView)

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

# Add data export view
admin.add_view(DataExportView(name='Data Export', endpoint='dataexport', category='System'))

app.register_blueprint(bp_room)
app.register_blueprint(bp_post)
app.register_blueprint(bp_auth)
app.register_blueprint(bp_user)
app.register_blueprint(bp_mail)
app.register_blueprint(bp_payment)


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

        logger.info("reload success %s", str(datetime.datetime.now())[:19])
        return "reload success"


def git_pull():
    repo = Repo(config.BASE_DIR)
    git = repo.git

    logger.info("当前未跟踪文件: %s", repo.untracked_files)
    logger.info("当前本地git仓库状态: %s", git.status())
    logger.info("当前本地git仓库是否有文件更新: %s", repo.is_dirty())
    logger.info("当前本地分支: %s", git.branch())
    logger.info("当前远程仓库: %s", git.remote())

    remote_name = "origin"
    logger.info("正在 git pull %s master", remote_name)
    git.pull(remote_name, "master")
    logger.info("拉取修改 %s 成功！", remote_name)


def send_post_survey_emails_for_room(room):
    message = '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Take the Exit Survey and Earn an Additional $5</title>
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
            <p>Thank you for participating on Chattera! We wanted to remind you that there is a post-survey available for you to complete. By completing this post-survey, you will earn an additional $5 as part of your compensation.</p>
            <p>To access the post-survey, simply click the button below.</p>
            <div style="margin: 30px 15px;">
              <a class="login-button" href="https://uwmadison.co1.qualtrics.com/jfe/form/SV_bQ3Ngp6xOKpXbds">Start the Survey</a>
            </div>
            <p>We greatly appreciate your time and participation so far, and your responses to the post-survey will be incredibly valuable to our team.</p>
            <p>Thank you once again!</p>
            </br>
            <p>Best regards,</p>
            <p>Your Chattera Team</p>
        </div>
        </body>
        </html>
        '''
    room_members = RoomMember.query.filter_by(room_id=room.id).all()
    email_list = []
    for member in room_members:
        user = User.query.filter_by(id=member.user_id).first()
        if user.email is not None:
            email_list.append({
                'recipients': [user.email],
                'subject': "Take the Exit Survey and Earn an Additional $5",
                'body': message,
                'html_body': message
            })

    if email_list:
        logger.info(f'Sending {len(email_list)} post-survey emails for room {room.id}')
        from mail_async import send_bulk_emails_async
        send_bulk_emails_async(email_list)
    else:
        logger.warning(f'No valid emails to send for room {room.id}')


def mail_morning():
    """
    Morning mail定时任务函数
    注意：此函数由APScheduler调度器调用，不需要Flask request上下文
    """
    try:
        logger.info("=" * 80)
        logger.info("Morning mail task started")
        logger.info("=" * 80)
        
        subject = 'mail_morning'

        rooms = Room.query.filter_by(activated=1).all()
        logger.info(f'Found {len(rooms)} activated rooms')
        for room in rooms:
            logger.info(f'Processing room {room.id}')
            # get topics
            room = Room.query.get(room.id)
            activated_at = room.activated_at
            if activated_at is None:
                continue
            local_time = time.localtime(int(activated_at.timestamp()))
            activated_day = local_time.tm_yday
            activated_year = local_time.tm_year
            logger.info('activated_day = %d', activated_day)

            now = time.localtime(time.time())
            now_day = now.tm_yday
            now_year = now.tm_year
            logger.info('now_day = %d', now_day)

            if now_year > activated_year:
                n = now_day + 365 - activated_day + 1
            else:
                n = now_day - activated_day + 1

            if n > 9:
                continue

            # 输出room.id、day
            logger.info('room.id = %d day = %d', room.id, n)
            if n == 9:
                continue

            # mail_template_morning = MailTemplate.query.filter_by(room_id=room.id).filter_by(day=n).filter_by(mail_type=1).first()
            mail_template_morning = MailTemplate.query.filter_by(mail_type=1, day=n).first()
            if mail_template_morning is None:
                logger.warning(f'No morning mail template found for room {room.id} day {n}')
                continue

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
                    <p>Good morning! Welcome back to Chattera! We value your contributions and encourage you to log in, join the discussion, and connect with the community.</p>
                    <p>%s</p>
                </div>
                <div style="margin: 30px 15px;">
                  <a class="login-button" href="https://camer-covid.journalism.wisc.edu/">Return to Chattera</a>
                </div>
                </body>
                </html>
            '''

            # message = PollPost.query.filter_by(
            #     room_id=room.id,
            #     topic=n
            # ).first()

            # if message is not None:
            #     photo_uri = 'http://ysj_5.soulfar.com/uploads/' + message.photo_uri
            # else:
            #     photo_uri = 'http://ysj_5.soulfar.com/uploads/daily_poll.jpeg'

            # img_str = photo_uri

            # message = message_html % (mail_template_morning.content)
            message = message_html % (mail_template_morning.content)
            room_members = RoomMember.query.filter_by(room_id=room.id).all()
            
            # 准备批量邮件列表
            email_list = []
            for member in room_members:
                subject = 'Chattera Morning Digest - DAY ' + str(n)
                user = User.query.filter_by(id=member.user_id).first()
                if user.email is not None:
                    email_list.append({
                        'recipients': [user.email],
                        # 'recipients': ['ch.zhuoqi@gmail.com'],
                        'subject': subject,
                        'body': message,
                        'html_body': message
                    })
            
            # 异步批量发送邮件
            if email_list:
                logger.info(f'Sending {len(email_list)} morning emails for room {room.id}')
                from mail_async import send_bulk_emails_async
                send_bulk_emails_async(email_list)
            else:
                logger.warning(f'No valid emails to send for room {room.id}')
        
        logger.info("Morning mail task completed successfully")
        logger.info("=" * 80)
    except Exception as e:
        logger.exception(f"Error in morning mail task: {str(e)}")
        raise


@app.route('/mail_morning')
def mail_morning_route():
    """HTTP路由版本的morning mail，用于手动触发测试"""
    with app.app_context():
        mail_morning()
        return jsonify({"status": "success", "message": "Morning mail sent"})


def mail_morning_day9():
    """
    Day 9 post-survey mail定时任务函数
    注意：此函数由APScheduler调度器调用，不需要Flask request上下文
    """
    try:
        logger.info("=" * 80)
        logger.info("Morning day 9 post-survey mail task started")
        logger.info("=" * 80)

        rooms = Room.query.filter_by(activated=1).all()
        logger.info(f'Found {len(rooms)} activated rooms')
        for room in rooms:
            logger.info(f'Processing room {room.id}')
            room = Room.query.get(room.id)
            activated_at = room.activated_at
            if activated_at is None:
                continue
            local_time = time.localtime(int(activated_at.timestamp()))
            activated_day = local_time.tm_yday
            activated_year = local_time.tm_year

            now = time.localtime(time.time())
            now_day = now.tm_yday
            now_year = now.tm_year

            if now_year > activated_year:
                n = now_day + 365 - activated_day + 1
            else:
                n = now_day - activated_day + 1

            if n != 9:
                continue

            send_post_survey_emails_for_room(room)

        logger.info("Morning day 9 post-survey mail task completed successfully")
        logger.info("=" * 80)
    except Exception as e:
        logger.exception(f"Error in morning day 9 post-survey mail task: {str(e)}")
        raise


def mail_night():
    """
    Night mail定时任务函数
    注意：此函数由APScheduler调度器调用，不需要Flask request上下文
    """
    try:
        logger.info("=" * 80)
        logger.info("Night mail task started")
        logger.info("=" * 80)
        
        # 指定服务器时区
        server_timezone = pytz.timezone('America/Chicago')

        # 获取当前服务器时间
        server_time = datetime.datetime.now(server_timezone)

        # 获取日期部分
        today = server_time.date()
        tomorrow = today + datetime.timedelta(days=1)

        # room activate day
        rooms = Room.query.filter_by(activated=1).all()
        logger.info(f'Found {len(rooms)} activated rooms')
        for room in rooms:
            day_activated = room.activated_at
            if day_activated is None:
                logger.warning(f'Room {room.id} has no activated_at timestamp, skipping')
                continue
            # FIXME 解决本地时间和服务器时间不一致问题
            local_time = time.localtime(int(day_activated.timestamp()))
            activated_day = local_time.tm_yday
            activated_year = local_time.tm_year
            logger.info('activated_day = %d', activated_day)

            now = time.localtime(time.time())
            now_day = now.tm_yday
            now_year = now.tm_year
            logger.info('now_day = %d', now_day)

            if now_year > activated_year:
                day = now_day + 365 - activated_day + 1
            else:
                day = now_day - activated_day + 1
            if day > 8:
                logger.info(f'Room {room.id} day {day} exceeds 8 days, skipping')
                continue
            room_members = RoomMember.query.filter_by(room_id=room.id).all()
            member_ids = []
            post_str = ""
            for member in room_members:
                member_ids.append(member.user_id)

            top = get_top_participants(room.id, today, tomorrow)
            top_str = ''''''
            if top and len(top) > 0:
                top_str += '<div class="container">'
                top_str += '<p class="title">Top Participants</p>'
                for i in range(len(top)):
                    user_id = top[i]['user_id']
                    user = User.query.filter_by(id=user_id).first()
                    top_str += '<p>' + user.nickname + ': ' + str(top[i]['total_count']) + ' Post/Comment</p>'
                top_str += '</div>'

            public_post_count = PublicPost.query.filter(
                PublicPost.room_id == room.id,
                PublicPost.topic == day,
                PublicPost.is_system_post != 1
            ).count()
            public_posts = PublicPost.query.filter_by(
                room_id=room.id,
                topic=day,
                is_system_post=0
            ).order_by(desc(PublicPost.created_at)).limit(5).all()

            post_str = '''<div class="container">'''
            post_str += '<p class="title">New posts: %d</p>'

            if public_post_count > 0:
                for post in public_posts:
                    user = User.query.filter_by(id=post.user_id).first()
                    post_words = post.post_content.split()
                    logger.debug('post_words[:10] = %s', post_words[:10])
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
                    logger.debug('system post_words[:10] = %s', post_words[:10])
                    post_str += "<p>Flashbacks: " + ' '.join(post_words[:10]) + "......</p>"
            post_str += "</div>"

            post_str = post_str % (public_post_count + system_post_count)

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
                    comment_words = comment.comment_content.split()
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
                <div>%s</div>
                </div>
                <!-- Top data -->
                  %s
                <!-- posts -->
                  %s
                <!-- comments -->
                  %s
                <!-- likes -->
                  %s
                <div style="margin: 30px 15px;">
                  <a class="login-button" href="https://camer-covid.journalism.wisc.edu/">Return to Chattera</a>
                </div>
                </body>
                </html>
            '''

            date_start = room.activated_at
            # date_start = datetime.datetime(2024, 1, 1, 0, 0)
            date_end = datetime.datetime.now()
            payments = calculate_func(room.id, date_start, date_end)

            for member in room_members:
                # 根据早晚类型及天数获取邮件模板
                # message_template = MailTemplate.query.filter_by(room_id=room.id, mail_type=2,
                #                                                 day=day).first()  # type=2: night mail template
                message_template = MailTemplate.query.filter_by(mail_type=2,
                                                                day=day).first()  # type=2: night mail template
                if message_template is None:
                    logger.warning("No mail template for room %d", room.id)
                    continue
                # TODO add payment
                if member.user_id in payments['total_rewards']:
                    payment = payments['total_rewards'][member.user_id]
                else:
                    payment = 0

                content = message_template.content
                topic = None
                if 1 <= day <= len(config.TOPIC_LIST):
                    topic = config.TOPIC_LIST[day - 1]
                else:
                    logger.warning("No topic configured for day %d in room %d", day, room.id)

                # 替换模板中的占位符：第一个 %s 是 payment，第二个 %s 是 topic
                if "%s" in content:
                    try:
                        # 计算模板中 %s 的数量
                        placeholder_count = content.count("%s")
                        if placeholder_count == 2 and topic is not None:
                            content = content % (payment, topic)
                        elif placeholder_count == 1:
                            # 只有一个占位符，根据模板内容判断替换 payment 还是 topic
                            if "$%s" in content:
                                content = content % payment
                            elif topic is not None:
                                content = content % topic
                        else:
                            logger.warning(
                                "Mail template has %d placeholders but topic is %s for room %d day %d",
                                placeholder_count, topic, room.id, day
                            )
                    except (TypeError, ValueError) as exc:
                        logger.warning(
                            "Mail template format error for room %d day %d: %s",
                            room.id,
                            day,
                            exc,
                        )

                message = message_html % (content, top_str, post_str, comment_str, like_str)
                subject = message_template.title

                user = User.query.filter_by(id=member.user_id).first()
                if user is None:
                    continue
                if user.email is not None:
                    # 异步发送邮件
                    from mail_async import send_email_async
                    send_email_async([user.email], subject, message, message)
        
        logger.info("Night mail task completed successfully")
        logger.info("=" * 80)
    except Exception as e:
        logger.exception(f"Error in night mail task: {str(e)}")
        raise


@app.route('/mail_night', methods=['GET'])
def mail_night_route():
    """HTTP路由版本的night mail，用于手动触发测试"""
    with app.app_context():
        mail_night()
        return jsonify({"status": "success", "message": "Night mail sent"})


@app.route('/post_experiment_summary_mail', methods=['POST'])
def post_experiment_summary_mail():
    data = request.get_json()
    room_ids = data['rooms']
    with app.app_context():
        # 指定服务器时区
        server_timezone = pytz.timezone('America/Chicago')
        # 获取当前服务器时间
        server_time = datetime.datetime.now(server_timezone)

        for room_id in room_ids:
            room = Room.query.filter_by(id=room_id).first()
            if room is None:
                continue
            day_activated = room.activated_at
            # FIXME 解决本地时间和服务器时间不一致问题
            local_time = time.localtime(int(day_activated.timestamp()))

            room_members = RoomMember.query.filter_by(room_id=room.id).all()
            member_ids = []
            post_str = ""
            for member in room_members:
                member_ids.append(member.user_id)

            date_start = local_time
            date_end = datetime.datetime.now()
            payments = calculate_func(room.id, date_start, date_end)

            for member in room_members:
                # TODO add payment
                if member.user_id not in payments['total_rewards']:
                    continue

                calculate_result = calculate_func(room_id, date_start, date_end)
                reward_summary = calculate_result['reward_summary']
                total_rewards = calculate_result['total_rewards']
                user = User.query.filter_by(id=member.user_id).first()
                formatted_data = format_data_for_user(
                    nickname=user.nickname,
                    user_id=member.user_id,
                    pre_survey_base=1,
                    post_survey_base=0,
                    reward_summary=reward_summary,
                    total_rewards=total_rewards
                )

                subject = 'Post-experiment summary'
                message = render_template("payment_mail.html", data=formatted_data)

                # logger.debug('formatted_data: %s', formatted_data)

                # return render_template("payment_mail.html", data=formatted_data)

                user = User.query.filter_by(id=member.user_id).first()
                if user.email is not None:
                    # 异步发送邮件
                    from mail_async import send_email_async
                    # 注意：这里保持测试邮箱，如果需要发送给真实用户，改为 [user.email]
                    # send_email_async(['cenux1987@163.com'], subject, message, message)
                    send_email_async([user.email], subject, message, message)

        return jsonify(Resp(result_code=2000, result_msg="success", data=None).__dict__)


@app.route('/test_post_experiment_summary_mail', methods=['GET'])
def test_post_experiment_summary_mail():
        # 指定服务器时区
        server_timezone = pytz.timezone('America/Chicago')
        # 获取当前服务器时间
        server_time = datetime.datetime.now(server_timezone)
        # 获取日期部分
        room = Room.query.get(45)
        day_activated = room.activated_at
        # FIXME 解决本地时间和服务器时间不一致问题
        local_time = time.localtime(int(day_activated.timestamp()))

        room_members = RoomMember.query.filter_by(room_id=room.id).all()
        member_ids = []
        post_str = ""
        for member in room_members:
            member_ids.append(member.user_id)

        date_start = datetime.datetime(2024, 1, 1)
        date_end = datetime.datetime.now()
        payments = calculate_func(room.id, date_start, date_end)

        for member in room_members:
            # TODO add payment
            if member.user_id not in payments['total_rewards']:
                continue

            logger.info('member\'s user id is %s', member.user_id)
            calculate_result = calculate_func(room.id, date_start, date_end)
            reward_summary = calculate_result['reward_summary']
            total_rewards = calculate_result['total_rewards']
            user = User.query.filter_by(id=member.user_id).first()
            formatted_data = format_data_for_user(
                nickname=user.nickname,
                user_id=member.user_id,
                pre_survey_base=1,
                post_survey_base=0,
                reward_summary=reward_summary,
                total_rewards=total_rewards
            )

            subject = 'Post-experiment summary'
            message = render_template("payment_mail.html", data=formatted_data)

            return render_template("payment_mail.html", data=formatted_data)


def format_data_for_user(nickname, user_id, pre_survey_base, post_survey_base, reward_summary, total_rewards):
    # 初始化 data 结构
    data = {
        "user_name": nickname,
        "pre_survey_base": pre_survey_base,
        "total_rewards": 0,
        "post_survey_base": post_survey_base,
        "days": [],
        "total_compensation": 0
    }

    # 遍历 reward_summary 填充 daily 数据
    for date, users in reward_summary.items():
        for user in users:
            if user['user_id'] == user_id:  # 匹配当前用户
                data['total_rewards'] = total_rewards[user['user_id']]
                day_data = {
                    "day": date,
                    "post": user['post_count'],
                    "share": user['share_count'],
                    "comment": user['comment_count'],
                    "base": 0.25 if user['daily_reward'] > 0 else 0.0,
                    "bonus": 1 if user['is_top_two'] else 0,
                    "total": user['daily_reward']
                }
                data["days"].append(day_data)

    # 计算总补偿值
    data["total_compensation"] = (
        sum(day["total"] for day in data["days"]) +
        pre_survey_base +
        post_survey_base
    )

    return data


@app.route('/test_night_mail_content', methods=['GET'])
def test_night_mail_content():
    # 指定服务器时区
    server_timezone = pytz.timezone('America/Chicago')

    # 获取当前服务器时间
    server_time = datetime.datetime.now(server_timezone)

    # 获取日期部分
    today = server_time.date()
    tomorrow = today + datetime.timedelta(days=1)

    # room activate day
    room = Room.query.get(46)
    day_activated = room.activated_at
    # FIXME 解决本地时间和服务器时间不一致问题
    local_time = time.localtime(int(day_activated.timestamp()))
    activated_day = local_time.tm_yday
    activated_year = local_time.tm_year
    logger.info('activated_day = %d', activated_day)

    now = time.localtime(time.time())
    now_day = now.tm_yday
    now_year = now.tm_year
    logger.info('now_day = %d', now_day)

    if now_year > activated_year:
        day = now_day + 365 - activated_day + 1
    else:
        day = now_day - activated_day + 1

    room_members = RoomMember.query.filter_by(room_id=room.id).all()
    member_ids = []
    post_str = ""
    for member in room_members:
        member_ids.append(member.user_id)

    top = get_top_participants(room.id, today, tomorrow)
    top_str = '''<div class="container">'''
    if top is not None and len(top) > 0:
        for i in range(len(top)):
            top_str += '<p class="title">Top Participants</p>'
            user_id = top[i]['user_id']
            user = User.query.filter_by(id=user_id).first()
            top_str += '<p>' + user.nickname + ': ' + str(top[i]['total_count']) + ' Post/Comment</p>'
    top_str += '</div>'

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
            logger.debug('post_words[:10] = %s', post_words[:10])
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
            logger.debug('system post_words[:10] = %s', post_words[:10])
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
            comment_words = comment.comment_content.split()
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
                <div>%s</div>
                </div>
                <!-- Top data -->
                  %s
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

    # day_start: activate day
    # day_end: today

    # room.activated_at get date
    date_start = room.activated_at
    # date_start = datetime.datetime(2024, 1, 1, 0, 0)
    date_end = datetime.datetime.now()
    payments = calculate_func(room.id, date_start, date_end)

    for member in room_members:
        # 根据早晚类型及天数获取邮件模板
        # message_template = MailTemplate.query.filter_by(room_id=room.id, mail_type=2).first()  # type=2: night mail template
        message_template = MailTemplate.query.filter_by(mail_type=2, day=day).first()  # type=2: night mail template
        if message_template is None:
            logger.warning("No mail template for room %d", room.id)
            continue
        # TODO add payment
        if member.user_id in payments['total_rewards']:
            payment = payments['total_rewards'][member.user_id]
        else:
            payment = 0
        logger.info('payment: %s, user id: %s', payment, member.user_id)

        content = message_template.content
        topic = None
        if 1 <= day <= len(config.TOPIC_LIST):
            topic = config.TOPIC_LIST[day - 1]

        # 替换模板中的占位符：第一个 %s 是 payment，第二个 %s 是 topic
        if "%s" in content:
            try:
                placeholder_count = content.count("%s")
                if placeholder_count == 2 and topic is not None:
                    content = content % (payment, topic)
                elif placeholder_count == 1:
                    if "$%s" in content:
                        content = content % payment
                    elif topic is not None:
                        content = content % topic
            except (TypeError, ValueError) as exc:
                logger.warning("Mail template format error: %s", exc)

        message = message_html % (content, top_str, post_str, comment_str, like_str)

        return message

@app.route('/top', methods=['GET'])
def test_count():
    room_id = request.args.get('room_id')

    top_n_results = get_top_participants(room_id)

    return jsonify(top_n_results)


with app.app_context():
    mail_template_morning = MailTemplate.query.filter_by(mail_type=1).first()
    
    # 创建带有app context的包装函数
    def mail_morning_job():
        """包装函数，确保在app context中执行"""
        with app.app_context():
            mail_morning()

    def mail_morning_day9_job():
        """包装函数，确保在app context中执行"""
        with app.app_context():
            mail_morning_day9()
    
    def mail_night_job():
        """包装函数，确保在app context中执行"""
        with app.app_context():
            mail_night()
    
    # 注册定时任务
    logger.info("=" * 80)
    logger.info("Registering scheduled jobs...")
    
    scheduler.add_job(
        func=mail_morning_job,
        trigger='cron',
        hour=7,
        id='job_mail_morning',
        name='Morning Mail Task',
        replace_existing=True
    )
    logger.info(f"✓ Morning mail job registered: trigger at hour 7")

    scheduler.add_job(
        func=mail_morning_day9_job,
        trigger='cron',
        hour=7,
        id='job_mail_morning_day9',
        name='Morning Day 9 Post-Survey Mail Task',
        replace_existing=True
    )
    logger.info("✓ Morning day 9 post-survey mail job registered: trigger at hour 7")
    
    scheduler.add_job(
        func=mail_night_job,
        trigger='cron',
        hour=22,
        id='job_mail_night',
        name='Night Mail Task',
        replace_existing=True
    )
    logger.info(f"✓ Night mail job registered: trigger at hour 22")
    
    # 打印所有注册的任务
    jobs = scheduler.get_jobs()
    logger.info(f"Total scheduled jobs: {len(jobs)}")
    for job in jobs:
        logger.info(f"  - Job ID: {job.id}, Next run: {job.next_run_time}")
    logger.info("=" * 80)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
