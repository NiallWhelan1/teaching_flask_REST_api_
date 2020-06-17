from flask_restful import Resource
from flask_jwt import jwt_required

from models.store import StoreModel

class Store(Resource):

	@jwt_required()
	def get(self, name):
		store = StoreModel.find_by_name(name)

		if store:
			return store.json(), 200 
		return {'message': 'Store not found'}, 404

	@jwt_required()
	def post(self, name):
		if StoreModel.find_by_name(name):
			return {'message': f'Store {name} already exists'}, 400

		store = StoreModel(name)
		try:
			store.save_to_db()
		except:
			{'message': 'Issue saving store to db'}, 500

		return store.json(), 201

	@jwt_required()
	def delete(self, name):
		store = StoreModel.find_by_name(name)

		if store:
			try:
				store.delete_from_db()
			except:
				{'message': 'Issue deleting store from db'}, 500
			return {'message': 'Store deleted successfully'}, 200

		return {'message': 'Store not found in db'}, 400


class StoreList(Resource):
	@jwt_required()
	def get(self):
		return {'stores': [store.json() for store in StoreModel.query.all()]}

		