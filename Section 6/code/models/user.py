import sqlite3
from database import db

class UserModel(db.Model):

	## Define Table Name for SQLAlchemy
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key = True) ## Note that id is auto generated (incrementally) in the DB as its a PK and Integer
	username = db.Column(db.String(80)) ## Limited to 80 chars
	password = db.Column(db.String(80))


	def __init__(self, username, password):
		self.username = username
		self.password = password

	def json(self):
		return {'id':self.id, 'username': self.username, 'prpasswordice': self.password}

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	@classmethod ## used with cls input - if change the class name (above) in the future, the function wont be impacted
	def find_by_username(cls, username):
		return cls.query.filter_by(username = username).first()


	@classmethod ## used with cls input - if change the class name (above) in the future, the function wont be impacted
	def find_by_id(cls, id):
		return cls.query.filter_by(id = id).first()