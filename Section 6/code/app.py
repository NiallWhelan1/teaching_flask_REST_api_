from flask import Flask
from flask_restful import Api 
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister, UserList
from resources.item import Item, ItemList
from resources.store import Store, StoreList

from database import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False ## Turns of Flask Modification tracker - we use the SQL Alchemy Tracker instead as its better

app.secret_key = 'niall'
api = Api(app)

## Create Database
@app.before_first_request
def create_tables():
	db.create_all()

jwt = JWT(app, authenticate, identity) # Create a new endpoint /auth

## Store Endpoints
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
## Item Endpoints
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
## User Endpoints
api.add_resource(UserRegister, '/register')
api.add_resource(UserList, '/users')

if __name__ == '__main__':
	db.init_app(app)

	app.run(host = '127.0.0.1',	
			port = 5000,
			debug = True
			)



