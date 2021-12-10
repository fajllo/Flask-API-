from flask_jwt_extended import create_access_token,create_refresh_token, get_jwt_identity
from flask_restful import Resource, reqparse
from models.user import UserModel
from flask_jwt_extended import jwt_required
import hmac


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {"message": "User with that username already exists."}, 400

        user = UserModel(data['username'], data['password'])
        user.save_to_db()
        return {"message": "User created successfully."}, 201

class UserDetails(Resource):

    jwt_required()
    def get(self, name):

        user = UserModel.find_by_username(name)
        if user:
            return user.json()
        return {"mesage": "user not found"}

    @jwt_required()
    def delete(self, name):
        user = UserModel.find_by_username(name)
        if user:
            user.delete_from_db()
            return {'message' : 'user deleted'}

        return {'message': 'no user to deleted'}


class UserAuth(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    @classmethod
    def post(cls):
        data = cls.parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        if user and hmac.compare_digest(data['password'],user.password):
            access_token = create_access_token(identity=user.id,fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token' : access_token,
                'refresh_token' : refresh_token
            },200

        return {'message': 'invalid credentials'},401



class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token},200
