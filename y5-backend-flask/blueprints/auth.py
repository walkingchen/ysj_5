from flasgger import swag_from
from flask import Blueprint, request, redirect, current_app, flash, json
from flask_login import login_required, logout_user, login_user, LoginManager, current_user
from flask_mail import Message
from flask_principal import identity_changed, Identity

from entity.Resp import Resp
from extensions import db, mail
from models import User, RoomMember, Room, Serializer

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
    except KeyError:
        return json.dumps(Resp(result_code=4000, result_msg='KeyError', data=None).__dict__)
    except TypeError:
        return json.dumps(Resp(result_code=4000, result_msg='TypeError', data=None).__dict__)

    user = User.query.filter_by(email=email).first()
    if user is not None:
        return json.dumps(Resp(result_code=4010, result_msg='Email already exists.', data=None).__dict__)

    user = User(
        email=email,
        # username=username,
        nickname=nickname,
        avatar=avatar,
        password=password
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
    subject = "Registration Confirmation"
    if user.email is not None:
        msg = Message(recipients=[user.email],
                      body=message,
                      subject=subject,
                      sender=("Admin", "sijia.yang@alumni.upenn.edu"))

        mail.send(msg)

    return json.dumps(Resp(result_code=2000, result_msg='register success', data=None).__dict__)


@swag_from('../swagger/auth/login.yaml')
@bp_auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    try:
        email = str(data['email']).strip()
        # username = str(data['username']).strip()
        password = str(data['password']).strip()
    except KeyError:
        return json.dumps(Resp(result_code=4000, result_msg='login, KeyError', data=None).__dict__)
    except TypeError:
        return json.dumps(Resp(result_code=4000, result_msg='login, TypeError', data=None).__dict__)

    user = User.query.filter_by(email=email).first()

    if user is None or password is None or password != user.password:
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
    return User.query.filter_by(id=user_id).first()


@login_required
@swag_from('../swagger/auth/logout.yaml')
@bp_auth.route('/logout')
def logout():
    logout_user()

    return json.dumps(Resp(result_code=2000, result_msg='success', data=None).__dict__)
