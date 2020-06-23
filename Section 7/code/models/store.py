from database import db

class StoreModel(db.Model):

	## Define Table Name for SQLAlchemy
	__tablename__ = 'stores'

	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(80))

	## Leverages Foreign Key in the items table
	items = db.relationship('ItemModel', lazy = 'dynamic') ## Will be a list as this is a many to one relationship
	## lazy means the relationship wont be created until it is called specifically (you then need to use items.all() to access)

	def __init__(self, name):
		self.name = name


	def json(self):
		return {'id':self.id, 'name': self.name, 'items': [item.json() for item in self.items.all() ]}


	@classmethod ## Allows us to call using self.find_by_name() or Item.find_by_name()
	def find_by_name(cls, name):
		return cls.query.filter_by(name = name).first() ## Select * FROM items WHERE name = <name> LIMIT 1


	def save_to_db(self):
		db.session.add(self)
		db.session.commit()
	
	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()
