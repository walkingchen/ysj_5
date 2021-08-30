from flasgger import swag_from
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource

from entity.Resp import Resp

bp_user = Blueprint('/api/user', __name__)
api = Api(bp_user, '/api/user')


class UserApi(Resource):
    pass


class UserUploadApi(Resource):
    @swag_from('../swagger/post/photo/create.yaml')
    def post(self):
        if request.method == 'POST' and 'file' in request.files:
            f = request.files.get('file')

        return jsonify(Resp(result_code=4000, result_msg="param error?", data=None).__dict__)


api.add_resource(
    UserUploadApi,
    '/',
    methods=['POST'],
    endpoint='post/photo/create')