from flask_restful import Resource, reqparse
from models.user import UserModel
from flask_jwt import jwt_required


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