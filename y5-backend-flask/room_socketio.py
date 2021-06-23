from flask import request, jsonify
from flask_socketio import emit, join_room, leave_room, send, Namespace

from extensions import db
from models import Message, User, Room

ROOM_PUBLIC = 0
ROOM_PRIVATE_CHAT = 1


class RoomNamespace(Namespace):
    def on_connect(self):
        print('socket connected')
        emit('connected', {'data': {'sid': request.sid}})

    def on_room_join(self, json):
        try:
            print(json)
            room_id = json['room_id']
            # print("room_id = " + room_id)
            join_room(room_id)
            emit('broadcast_msg', request.sid + " join in room " + room_id, room=room_id)
        except KeyError:
            print('room socketio: KeyError')
        except TypeError:
            print('room socketio: TypeError')

    # def on_message(self, message):
    #     try:
    #         room_id = message['room_id']
    #         print("room_id = " + room_id)
    #         emit('new_post', {}, room=room_id)
    #     except KeyError:
    #         pass
    #     except TypeError:
    #         pass

    def on_room_leave(self, message):
        room_id = message['room_id']
        leave_room(room_id)


class ChatNamespace(Namespace):
    def on_connect(self):
        emit('connected', {'data': {'sid': request.sid}})

    def on_join(self, message):
        print(message)

    # def on_message(self, message):
    #     print(message)
    #     user_id_from = message['user_from']
    #     user_id_to = message['user_to']
    #     message = message['message']
    #     room_id = message['room_id']
    #
    #     user_from = User.query.filter_by(id=user_id_from).first()
    #     user_to = User.query.filter_by(id=user_id_to).first()
    #     room = Room.query.filter_by(id=room_id).first()
    #
    #     if room is None or user_from is None or user_to is None:
    #         return
    #
    #     print(room.room_name + ', ' + user_from.username + ' says to ' + user_to.username + ': ' + message)
    #     message = Message(
    #         message=jsonify(message),
    #         message_type=0,
    #         room_id=room_id,
    #         user_id_from=user_id_from,
    #         user_id_to=user_id_to
    #     )
    #     db.session.add(message)
    #     db.session.commit()
    #     emit('broadcast_msg', message.message, room=room_id)

    def on_leave(self, message):
        print(message)
        username = message['username']
        room = message['room']
        leave_room(room)
        send(username + ' has left the room.', room=room)