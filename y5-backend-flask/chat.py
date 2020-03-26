import socketio
from flask_socketio import emit, join_room, leave_room, send

from app import cache
from extensions import db
from models import Message


@socketio.on('join')
def on_join(data):
    username = data['username'] # data['KEY_NAME'] == data.KEY_NAME
    room = data['room']

    _room_list = cache.get('room_list')
    if _room_list is None:
        _room_list = []
    if room not in _room_list:
        _room_list.append(room)
        cache.set('room_list', _room_list)
        print(cache.get('room_list'))
        emit('room_list', _room_list)

    join_room(room)
    emit('broadcast_msg', data, room=room)


@socketio.on('msg')
def on_msg(data):
    author = data['author']
    message = data['message']
    room = data['room']
    print(author + ' in ' + room + ' says: ' + data['message'])
    message = Message(
        author=author,
        message=message
    )
    db.session.add(message)
    db.session.commit()
    res = {
        'author': author,
        'message': message
    }
    emit('broadcast_msg', res, room=room)


@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the room.', room=room)
