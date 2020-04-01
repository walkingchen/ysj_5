from flask import request
from flask_socketio import emit, join_room, leave_room, send, Namespace

from extensions import db
from models import Message, User, Room

ROOM_PUBLIC = 0
ROOM_PRIVATE_CHAT = 1


class ChatRoomNamespace(Namespace):
    def on_connect(self):
        emit('connected', request.sid)

    def on_join(self, message):
        print(message)
        try:
            user_id = message['user_id']
            room_id = int(message['room_id'])
            room_type = int(message['room_type'])

            if room_type == ROOM_PUBLIC:  # 聊天室
                join_room(room_id)
            elif room_type == ROOM_PRIVATE_CHAT:   # 私聊
                join_room(room_id)
                emit('broadcast_msg', message, room=room_id)
            else:
                emit('broadcast_msg', message, room=room_id)
        except KeyError:
            pass
        except TypeError:
            pass

    def on_my_event(self, message):
        print('received message: ' + message['username'])

    def on_msg(self, message):
        print(message)
        user_id_from = message['user_from']
        user_id_to = message['user_to']
        message = message['message']
        room_id = message['room_id']

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

    def on_leave(self, message):
        print(message)
        username = message['username']
        room = message['room']
        leave_room(room)
        send(username + ' has left the room.', room=room)
