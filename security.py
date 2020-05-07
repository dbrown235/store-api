from werkzeug.security import safe_str_cmp
from models.user import UserModel


def authenticate(username, password):
    # 1. put in user name, get user object
    user = UserModel.find_by_username(username)  # username is key get method assigns value to user
    # 2. compare input password with password we have in object
    if user and safe_str_cmp(user.password, password):
        return user


# unique to flask-jwt, takes in payload (contents of jwt token) extract
def identity(payload):
    user_id = payload['identity']  # extract userid from payload
    return UserModel.find_by_id(user_id)  # return object using extracted userid
