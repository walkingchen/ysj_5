class RoomResp:
    room = None
    posts_pub = []
    posts_pri = []

    def __init__(self, room, posts_pub, posts_pri):
        self.room = room
        self.posts_pub = posts_pub
        self.posts_pri = posts_pri
