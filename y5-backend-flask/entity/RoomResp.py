class RoomResp:
    room = None
    timeline_pub = None
    timeline_pri = None
    posts_pub = []
    posts_pri = []

    def __init__(self, room, timeline_pub, timeline_pri, posts_pub, posts_pri):
        self.room = room
        self.timeline_pub = timeline_pub
        self.timeline_pri = timeline_pri
        self.posts_pub = posts_pub
        self.posts_pri = posts_pri
