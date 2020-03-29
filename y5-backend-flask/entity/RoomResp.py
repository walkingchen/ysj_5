class RoomResp:
    room = None
    members = []
    posts_pub = []
    posts_pri = []

    def __init__(self, room, members):
        self.room = room,
        self.members = members
        # self.posts_pub = posts_pub
        # self.posts_pri = posts_pri
