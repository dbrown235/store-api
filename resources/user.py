import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser() # create new parser object
    parser.add_argument('username', type=str, required = True, help="This field cant be blank")
    parser.add_argument('password', type=str, required = True)

    def post(self):

        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {'message':'This user already exists'}, 400

        user = UserModel(**data) #for each of the keys pass in values
        user.save_to_db()

        return {"message":"User create successfully"}, 201