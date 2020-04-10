from flasgger import swag_from
from flask import Blueprint, request, redirect, current_app, flash, json
from flask_login import login_required, logout_user, login_user, LoginManager
from flask_principal import identity_changed, Identity

from entity.Resp import Resp
from extensions import db
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
        username = data['username']
        password = data['password']
    except KeyError:
        return json.dumps(Resp(result_code=4000, result_msg='KeyError', data=None).__dict__)
    except TypeError:
        return json.dumps(Resp(result_code=4000, result_msg='TypeError', data=None).__dict__)

    user = User.query.filter_by(email=email).first()
    if user is not None:
        return json.dumps(Resp(result_code=4000, result_msg='user exists', data=None).__dict__)

    user = User(
        email=email,
        username=username,
        password=password
    )
    db.session.add(user)
    db.session.commit()

    return json.dumps(Resp(result_code=2000, result_msg='register success', data=None).__dict__)


@swag_from('../swagger/auth/login.yaml')
@bp_auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    try:
        username = data['username']
        password = data['password']
    except KeyError:
        return json.dumps(Resp(result_code=4000, result_msg='KeyError', data=None).__dict__)
    except TypeError:
        return json.dumps(Resp(result_code=4000, result_msg='TypeError', data=None).__dict__)

    user = User.query.filter_by(username=username).first()

    if user is None or password is None or password != user.password:
        return json.dumps(Resp(result_code=4000, result_msg='fail', data=None).__dict__)

    # Keep the user info in the session using Flask-Login
    login_user(user)
    # Tell Flask-Principal the identity changed
    identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))
    # fixme 判断是否管理员
    # return redirect('/admin/')

    member = RoomMember.query.filter_by(user_id=user.id).first()
    room = Room.query.filter_by(id=member.room_id).first()

    return json.dumps(Resp(
        result_code=2000,
        result_msg='success',
        data=Serializer.serialize(room)
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
