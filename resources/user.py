from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash

from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="This field is required")
    parser.add_argument('password', type=str, required=True, help="This field is required")

    @classmethod
    def post(cls):
        data = cls.parser.parse_args()
        if UserModel.find_by_username(data.username):
            return {'message': f'User {data.username} already exists'}, 400
        user = UserModel(data.username, generate_password_hash(data.password))
        user.save_to_db()
        return data, 201
