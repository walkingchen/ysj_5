from models import Serializer


class RoomResp:
    members = []
    room = None
    redspot_list = []

    def __init__(self, room, members, redspot_list):
        self.room = room
        self.members = members
        self.redspot_list = redspot_list

    def serialize(self):
        d = Serializer.serialize(self)
        return d
