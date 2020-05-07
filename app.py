from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from db import db
# db is a SQLAlchemy object from the db file

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item,ItemList
from resources.store import Store,StoreList

# import resources will import models. models need to 'seen' in order for
# SQLAlchemy to create tables from column set up in models


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' #connection to db
app.config['SQLAlCHEMY_TRACK_MODIFICATIONS'] = False #tell Flask not to track modifications
app.secret_key = 'jose'
api = Api(app) #make flask conform to restful principles through flask_restful

#flask decorator
@app.before_first_request
def create_tables():
    db.create_all() #create all tables unless they exist already

#use created app object, authenticate function, and identity function
jwt = JWT(app, authenticate, identity)
# jwt creates a new endpoint (/auth)
# when we call /auth we send it a username and password and jwt get it and send it to
# auth - we use authenticate, and returns user object, jwt creates a token to the user



api.add_resource(Item, '/item/<string:name>') # http://127.0.0.1:5000/item/thing
api.add_resource(ItemList,'/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store,'/store/<string:name>')
api.add_resource(StoreList,'/stores')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port = 5000, debug=True)