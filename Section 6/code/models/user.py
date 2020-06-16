import sqlite3
from database import db

class UserModel(db.Model):

	## Define Table Name for SQLAlchemy
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(80)) ## Limited to 80 chars
	password = db.Column(db.String(80))


	def __init__(self, _id, username, password):
		self.id = _id
		self.username = username
		self.password = password


	@classmethod ## used with cls input - if change the class name (above) in the future, the function wont be impacted
	def find_by_username(cls, username):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query = "SELECT * FROM users WHERE username = ?"
		result = cursor.execute(query, (username,)) ## Requires a tuple input hence (username,)
		row = result.fetchone()

		connection.close()

		if row: ## same as - if row is not None:
			user = cls(*row) #user = cls(row[0], row[1], row[2]) 

		else:
			user = None

		return user


	@classmethod ## used with cls input - if change the class name (above) in the future, the function wont be impacted
	def find_by_id(cls, id):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query = "SELECT * FROM users WHERE id = ?"
		result = cursor.execute(query, (id,)) ## Requires a tuple input hence (id,)
		row = result.fetchone()

		connection.close()

		if row: ## same as - if row is not None:
			user = cls(*row) #user = cls(row[0], row[1], row[2]) 

		else:
			user = None


		return user