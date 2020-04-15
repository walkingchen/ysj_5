from models import Serializer


class RoomResp:
    members = []
    room = None

    def __init__(self, room, members):
        self.room = room
        self.members = members

    def serialize(self):
        d = Serializer.serialize(self)
        return d
