from flask import Flask, request
from flask_restful import Resource, Api, reqparse 
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'niall'
api = Api(app)

jwt = JWT(app, authenticate, identity) # Create a new endpoint /auth

items = []

class Item(Resource):

	## Specify what values are paresed from the request 
	### Creates a parser object
	parser = reqparse.RequestParser()
	parser.add_argument('price',
						type = float,
						required = True,
						help = 'This field cannot be left blank')	

	@jwt_required()
	def get(self, name):

		item = filter(lambda x: x['name'] == name, items)
		#item = list(filter) ## Creates a list as the return from a filter function is a filter object
		item = next(item,None) ## Returns the next item (first and only in this case)

		return ({'item': item}, 200 if item is not None else 404)

		''' ## list Implementation
		for item in items:
			if item['name'] == name:
				return item
		
		return {'item':'No item available by this name'}, 404
		'''

	#@jwt_required()
	def post(self, name):

		if next(filter(lambda x: x['name'] == name, items), None) is not None:
			return {'item': f'Item with name {name} already exists'}, 400

		data = Item.parser.parse_args()

		item = {'name':name,
				'price':data['price']}
		items.append(item)
		return item, 201


	def put(self, name):	

		data = Item.parser.parse_args()
		
		item = next(filter(lambda x: x['name'] == name, items), None)

		if item == None:
			item = {'name': name, 'price': data['price']}
			items.append(item)
		else:
			item.update(data) # updates the item

		return item



	def delete(self, name):
		global items
		items = list(filter(lambda x: x['name'] != name, items))
		return {'message': 'Item Deleted'}, 200


class Items(Resource):

	def get(self):
		return {"items": items} 

api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items/')

app.run(host = '127.0.0.1',	
		port = 5000,
		debug = True
		)