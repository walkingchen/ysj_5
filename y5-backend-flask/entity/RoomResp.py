class RoomResp:

    def __init__(self, room_serialized, room_members):
        self.room = dict(room_serialized),
        self.members = room_members
