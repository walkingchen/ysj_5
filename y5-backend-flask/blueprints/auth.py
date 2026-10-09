from flasgger import swag_from
import hashlib
import re
import secrets
from datetime import datetime, timedelta
from html import escape

from flask import Blueprint, request, redirect, current_app, flash, json
from flask_login import login_required, logout_user, login_user, LoginManager, current_user
from flask_principal import identity_changed, Identity
from sqlalchemy import func

from entity.Resp import Resp
from extensions import db
from models import User, RoomMember, Room, Serializer, PasswordResetToken
from mail_async import send_email_async, send_registration_email_async
from passwords import hash_password, verify_password

bp_auth = Blueprint('api/auth', __name__, url_prefix='/api/auth')

login_manager = LoginManager()
login_manager.login_view = 'login'


@swag_from('../swagger/auth/register.yaml')
@bp_auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    try:
        email = data['email']
        # username = data['username']
        nickname = data['nickname']
        avatar = data['avatar']
        password = data['password']
        rid = data.get('rid', None)
        sid = data.get('sid', None)
    except KeyError:
        return json.dumps(Resp(result_code=4000, result_msg='KeyError', data=None).__dict__)
    except TypeError:
        return json.dumps(Resp(result_code=4000, result_msg='TypeError', data=None).__dict__)

    user = User.query.filter_by(email=email).first()
    if user is not None:
        return json.dumps(Resp(result_code=4010, result_msg='Email already exists.', data=None).__dict__)

    user = User.query.filter_by(nickname=nickname).first()
    if user is not None:
        return json.dumps(Resp(result_code=4010, result_msg='Nickname already exists.', data=None).__dict__)

    user = User(
        email=email,
        # username=username,
        nickname=nickname,
        avatar=avatar,
        password=hash_password(password),
        rid=rid,
        sid=sid
    )
    db.session.add(user)
    db.session.commit()

    # TODO html message
    message = '''
Thank you for registering for Chattera and we’re excited to have you on board! 
We are currently working on setting up the platform for your participation. Once everything is ready, we will send you another email with the details for log-in and other logistic issues. At that point, you’ll be able to interact with other participants and start chatting!

If you have questions about this study, please reply to this email or contact us at chattera.platform@gmail.com

Thank you again for your participation, and we’ll be in touch soon!

Best regards,
Your Chattera Team
    '''
    # 异步发送注册确认邮件
    if user.email is not None:
        send_registration_email_async(user.email, user.nickname)

    return json.dumps(Resp(result_code=2000, result_msg='register success', data=None).__dict__)


@swag_from('../swagger/auth/login.yaml')
@bp_auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    try:
        email = str(data['email']).strip()
        # username = str(data['username']).strip()
        password = str(data['password'])
    except KeyError:
        return json.dumps(Resp(result_code=4000, result_msg='login, KeyError', data=None).__dict__)
    except TypeError:
        return json.dumps(Resp(result_code=4000, result_msg='login, TypeError', data=None).__dict__)

    user = User.query.filter_by(email=email).first()

    if user is None or not verify_password(user.password, password):
        return json.dumps(Resp(result_code=4000, result_msg='username or password wrong', data=None).__dict__)

    # Keep the user info in the session using Flask-Login
    login_user(user)
    # Tell Flask-Principal the identity changed
    identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))
    # fixme 判断是否管理员
    # return redirect('/admin/')

    members = RoomMember.query.filter_by(user_id=user.id, activated=1).all()
    if len(members) == 0:
        return json.dumps(Resp(
            result_code=2010,
            result_msg='Please wait for email notification',
            data=None
        ).__dict__)

    for member in members:
        room = Room.query.filter_by(id=member.room_id, activated=1).first()
        if room is not None:
            return json.dumps(Resp(
                result_code=2000,
                result_msg='success',
                data=Serializer.serialize(room)
            ).__dict__)

    return json.dumps(Resp(
        result_code=2010,
        result_msg='Room not activated, please wait for email notification, room id: %d' % member.room_id,
        data=None
    ).__dict__)


@login_manager.user_loader
def load_user(user_id):
    try:
        parts = str(user_id).split(':', 1)
        user = User.query.filter_by(id=int(parts[0])).first()
        if user is None:
            return None
        version = int(parts[1]) if len(parts) == 2 else 0
        return user if (user.session_version or 0) == version else None
    except (TypeError, ValueError):
        return None


RESET_REQUEST_MESSAGE = 'If an account exists for this email, a password reset link will be sent.'
RESET_TOKEN_LIFETIME = timedelta(minutes=30)
RESET_REQUEST_WINDOW = timedelta(hours=1)
RESET_REQUEST_COOLDOWN = timedelta(minutes=1)


def _reset_response(code, message):
    return json.dumps(Resp(result_code=code, result_msg=message, data=None).__dict__)


@bp_auth.route('/password-reset/request', methods=['POST'])
def request_password_reset():
    data = request.get_json(silent=True) or {}
    if not isinstance(data, dict):
        return _reset_response(4000, 'Please enter a valid email address.')
    email = data.get('email')
    if not isinstance(email, str):
        return _reset_response(4000, 'Please enter a valid email address.')
    email = email.strip().lower()
    if len(email) > 128 or not re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', email):
        return _reset_response(4000, 'Please enter a valid email address.')

    now = datetime.utcnow()
    email_hash = hashlib.sha256(email.encode('utf-8')).hexdigest()
    recent = (PasswordResetToken.query
              .filter(PasswordResetToken.email_hash == email_hash,
                      PasswordResetToken.created_at >= now - RESET_REQUEST_WINDOW)
              .order_by(PasswordResetToken.created_at.desc()).all())
    if len(recent) >= 3 or (recent and recent[0].created_at > now - RESET_REQUEST_COOLDOWN):
        return _reset_response(2000, RESET_REQUEST_MESSAGE)

    user = User.query.filter(func.lower(User.email) == email).first()
    token = secrets.token_urlsafe(32)
    if user is not None:
        (PasswordResetToken.query
         .filter(PasswordResetToken.user_id == user.id,
                 PasswordResetToken.used_at.is_(None))
         .update({'used_at': now}, synchronize_session=False))
    db.session.add(PasswordResetToken(
        user_id=user.id if user else None,
        email_hash=email_hash,
        token_hash=hashlib.sha256(token.encode('ascii')).hexdigest(),
        created_at=now,
        expires_at=now + RESET_TOKEN_LIFETIME,
    ))
    db.session.commit()

    if user is not None:
        reset_url = current_app.config['FRONTEND_URL'].rstrip('/') + '/#/reset-password?token=' + token
        body = ('We received a request to reset your Chattera password.\n\n'
                'Use this link within 30 minutes:\n{}\n\n'
                'If you did not request this, you can ignore this email.\n\n'
                'The Chattera Team').format(reset_url)
        html_body = ('<p>We received a request to reset your Chattera password.</p>'
                     '<p><a href="{}">Reset your password</a> (valid for 30 minutes).</p>'
                     '<p>If you did not request this, you can ignore this email.</p>'
                     '<p>The Chattera Team</p>').format(escape(reset_url, quote=True))
        send_email_async([user.email], 'Reset your Chattera password', body, html_body)
    return _reset_response(2000, RESET_REQUEST_MESSAGE)


@bp_auth.route('/password-reset/confirm', methods=['POST'])
def confirm_password_reset():
    data = request.get_json(silent=True) or {}
    if not isinstance(data, dict):
        return _reset_response(4000, 'This reset link is invalid or has expired.')
    token = data.get('token')
    password = data.get('password')
    if not isinstance(token, str) or len(token) > 128 or not token:
        return _reset_response(4000, 'This reset link is invalid or has expired.')
    if not isinstance(password, str) or not 12 <= len(password) <= 128:
        return _reset_response(4000, 'Password must be between 12 and 128 characters.')

    token_hash = hashlib.sha256(token.encode('utf-8')).hexdigest()
    now = datetime.utcnow()
    reset_token = (PasswordResetToken.query
                   .filter_by(token_hash=token_hash)
                   .with_for_update().first())
    if reset_token is None or reset_token.used_at is not None or reset_token.expires_at <= now or reset_token.user_id is None:
        return _reset_response(4000, 'This reset link is invalid or has expired.')
    user = User.query.filter_by(id=reset_token.user_id).with_for_update().first()
    if user is None:
        return _reset_response(4000, 'This reset link is invalid or has expired.')

    user.password = hash_password(password)
    user.session_version = (user.session_version or 0) + 1
    (PasswordResetToken.query
     .filter(PasswordResetToken.user_id == user.id,
             PasswordResetToken.used_at.is_(None))
     .update({'used_at': now}, synchronize_session=False))
    db.session.commit()
    logout_user()
    return _reset_response(2000, 'Your password has been reset. Please sign in.')


@login_required
@swag_from('../swagger/auth/logout.yaml')
@bp_auth.route('/logout')
def logout():
    logout_user()

    return json.dumps(Resp(result_code=2000, result_msg='success', data=None).__dict__)
