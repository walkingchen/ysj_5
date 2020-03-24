from flask import Blueprint

room = Blueprint('/room', __name__, url_prefix='/room')


@room.route('/', methods=['GET'])
def room():
    pass