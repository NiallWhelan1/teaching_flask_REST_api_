import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


class Item(Resource):

	## Specify what values are paresed from the request 
	### Creates a parser object
	parser = reqparse.RequestParser()
	parser.add_argument('price',
						type = float,
						required = True,
						help = 'This field cannot be left blank')	

	@classmethod ## Allows us to call using self.find_by_name() or Item.find_by_name()
	def find_by_name(cls, name):

		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query = "SELECT * FROM items WHERE name = ?"

		result = cursor.execute(query, (name,))
		row = result.fetchone()
		connection.close()

		if row:
			return {'item': {'name': row[0], 'price': row[1] }}


	@classmethod
	def insert(cls, item):

		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query = "INSERT INTO items VALUES(?, ?)"

		cursor.execute(query, (item['name'],item['price']) )

		connection.commit()
		connection.close()

	@classmethod
	def update(cls, item):

		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query = "UPDATE items SET price = ? WHERE name = ?"

		cursor.execute(query, (item['price'], item['name']) )

		connection.commit()
		connection.close()

	@jwt_required()
	def get(self, name):

		try:
			item = self.find_by_name(name)
		except:
			return {'message': 'Error occurred extracting item from DB'}, 500 ## Internal server Error

		if item:
			return item, 200
		return {'message': 'Item not found'} , 404


	#@jwt_required()
	def post(self, name):

		if self.find_by_name(name):
			return {'item': f'Item with name {name} already exists'}, 400

		data = Item.parser.parse_args()

		item = {'name':name,
				'price':data['price']}
		
		try:
			self.insert(item)
		except:
			return{'message': 'Error occurred inserting item into DB'}, 500 ## Internal server Error

		return item, 201


	def put(self, name):	

		data = Item.parser.parse_args()
		
		item = self.find_by_name(name)
		updated_item = {'name': name, 'price': data['price']}

		if item == None:
			
			try:
				self.insert(updated_item)
			except:
				return {'message': 'Database error when adding item'}, 500
		
		else:
			try:
				self.update(updated_item) # updates the item
			except:
				return {'message': 'Database error when updating the item'}, 500

		return updated_item



	def delete(self, name):
		
		if self.find_by_name(name):

			connection = sqlite3.connect('data.db')
			cursor = connection.cursor()

			query = "DELETE FROM items WHERE name = ?"

			cursor.execute(query, (name,) )

			connection.commit()
			connection.close()

			return {'message': 'Item Deleted'}, 200

		return {'message': 'Item not found, could not delete as it does not exist'}, 404


class ItemList(Resource):

	def get(self):

		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query = "SELECT * FROM items"

		items = []
		result =  cursor.execute(query)
		for row in result:
			items.append({'name': row[0], 'price': row[1]})

		connection.close()

		return {"items": items} 



