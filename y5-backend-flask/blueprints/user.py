import csv

from flasgger import swag_from
from flask import Blueprint, request, jsonify, send_from_directory
from flask_restful import Api, Resource

from entity.Resp import Resp
from models import User

bp_user = Blueprint('/api/user', __name__)
api = Api(bp_user, '/api/user')


class UserApi(Resource):
    pass


# class UserUploadApi(Resource):
#     @swag_from('../swagger/post/photo/create.yaml')
#     def post(self):
#         if request.method == 'POST' and 'file' in request.files:
#             f = request.files.get('file')
#
#         return jsonify(Resp(result_code=4000, result_msg="param error?", data=None).__dict__)
#
#
# api.add_resource(
#     UserUploadApi,
#     '/',
#     methods=['POST'],
#     endpoint='post/photo/create')


@swag_from('../swagger/user/export_user.yaml')
@bp_user.route('/api/user/export_user', methods=['GET'])
def export_room():
    users = User.query.all()
    with open('static/export_user.csv', 'w',  encoding='UTF-8', newline='') as f:
        csv_writer = csv.writer(f)
        # header = ['id', 'user_id', 'room_type', 'room_id', 'seat_no', 'day', 'topic_no', 'message_id']
        header = ['id', 'username', 'email', 'created_at']
        csv_writer.writerow(header)
        for user in users:
            line = [str(user.id), str(user.username), str(user.email), str(user.created_at)]
            csv_writer.writerow(line)

    return send_from_directory('static', 'export_user.csv', as_attachment=True)
