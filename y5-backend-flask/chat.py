from flask_socketio import emit, join_room, leave_room, send
from app import cache, socketio
from extensions import db
from models import Message, User, Room

ROOM_TYPE_ALL = 0
ROOM_TYPE_CHAT = 1


@socketio.on('join')
def on_join(data):
    try:
        user_id = data['user_id']
        room_id = int(data['room_id'])
        room_type = int(data['room_type'])

        if room_type == ROOM_TYPE_ALL:  # 聊天室
            room_list = cache.get('room_list')
            if room_list is None:
                room_list = []
            if room_id not in room_list:
                room_list.append(room_id)
                cache.set('room_list', room_list)
                print(cache.get('room_list'))
                emit('room_list', room_list)
        elif room_type == ROOM_TYPE_CHAT:   # 私聊
            join_room(room_id)
            emit('broadcast_msg', data, room=room_id)
        else:
            emit('broadcast_msg', data, room=room_id)
    except KeyError:
        pass
    except TypeError:
        pass


@socketio.on('msg')
def on_msg(data):
    user_id_from = data['user_from']
    user_id_to = data['user_to']
    message = data['message']
    room_id = data['room_id']

    user_from = User.query.filter_by(id=user_id_from).first()
    user_to = User.query.filter_by(id=user_id_to).first()
    room = Room.query.filter_by(id=room_id).first()

    if room is None:
        return

    if user_from is None or user_to is None:
        emit('broadcast_msg', message, room=room_id)
        return

    print(room.room_name + ', ' + user_from.username + ' says to ' + user_to.username + ': ' + message)
    message = Message(
        message=message,
        message_type=0,
        room_id=room_id,
        user_id_from=user_id_from,
        user_id_to=user_id_to
    )
    db.session.add(message)
    db.session.commit()
    emit('broadcast_msg', message.message, room=room_id)


@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the room.', room=room)
