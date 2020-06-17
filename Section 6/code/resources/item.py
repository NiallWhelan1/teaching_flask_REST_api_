from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel


class Item(Resource):

	## Specify what values are paresed from the request 
	### Creates a parser object
	parser = reqparse.RequestParser()
	parser.add_argument('price',
						type = float,
						required = True,
						help = 'This field cannot be left blank')
	parser.add_argument('store_id',
						type = int,
						required = True,
						help = 'Every item needs a store id')		

	@jwt_required()
	def get(self, name):

		try:
			item = ItemModel.find_by_name(name)
		except:
			return {'message': 'Error occurred extracting item from DB'}, 500 ## Internal server Error

		if item:
			return item.json(), 200
		return {'message': 'Item not found'} , 404

	@jwt_required()
	def post(self, name):

		if ItemModel.find_by_name(name):
			return {'item': f'Item with name {name} already exists'}, 400

		data = Item.parser.parse_args()

		item = ItemModel(name, **data) ##ItemModel(name, data['price'], data['store_id']) 
		
		try:
			item.save_to_db()
		except:
			return{'message': 'Error occurred inserting item into DB'}, 500 ## Internal server Error

		return item.json(), 201

	@jwt_required()
	def put(self, name):	

		data = Item.parser.parse_args()
		
		item = ItemModel.find_by_name(name)

		if item == None:		
			item = ItemModel(name, **data) ##ItemModel(name, data['price'], data['store_id']) 
		else:
			item.price = data['price']
			item.store_id = data['store_id']

		item.save_to_db()
		return item.json()

	@jwt_required()
	def delete(self, name):
		item = ItemModel.find_by_name(name)

		if item:
			item.delete_from_db()

			return {'message': 'Item Deleted'}, 200

		return {'message': 'Item not found, could not delete as it does not exist'}, 404


class ItemList(Resource):

	@jwt_required()
	def get(self):
		return {'items': [item.json() for item in ItemModel.query.all()]}
		## return {'items': list(map(lambda x: x.json(), ItemModel.query.all() ))} ## Same result with lambda function



