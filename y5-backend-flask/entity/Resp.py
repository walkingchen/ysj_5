from models import Serializer


class Resp:
    result_code = 2000
    result_msg = 'success'
    data = None

    def __init__(self, result_code, result_msg, data):
        self.result_code = result_code
        self.result_msg = result_msg
        self.data = data

    def serialize(self):
        d = Serializer.serialize(self)
        return d


