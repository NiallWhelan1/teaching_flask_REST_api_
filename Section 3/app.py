from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

stores = [
	{
	'name': 'My First Store',
	'items': [
			{
				'name': '1st Item',
				'price': 15.99

			}
 		]		
	}
]

 ## Hello World Homepage Example
@app.route('/') # Homepage of site/application
def home():
	return render_template('index.html') # Flask automatically looks for a templates folder


## This application is a server, therefore it sees requests as follows:
## POST: Used to recieve data 
## GET: Used to send data back only


# POST /store data: {name:}
@app.route('/store', methods = ['POST'])
def create_store():
	request_data = request.get_json()
	new_store = {
		'name': request_data['name'],
		'items': []
	}

	stores.append(new_store)

	return jsonify(new_store)


# GET /store/<string:name>
@app.route('/store/<string:name>', methods = ['GET']) ## http://127.0.0.1:5000/store/<some_name>
def get_store(name):
	
	for store in stores:
		if store['name'] == name:
			return jsonify(store)
	return jsonify({'message':'Store Not Found'})




# GET /store
@app.route('/store/') ## http://127.0.0.1:5000/store/<some_name>
def get_stores():
	return jsonify({'stores':stores}) # Must return a dictionary for JS to use as JSON 
									  # (Note our stores variable is a list)


# POST /store/<string:name>/item {name:, price:}
@app.route('/store/<string:name>/item', methods = ['POST'])
def create_item_in_store(name):
	for store in stores:
		if store['name'] == name:
			request_data = request.get_json()
			new_item = {
				'name': request_data['name'],
				'price': request_data['price']
			}
			store['items'].append(new_item)
			return jsonify(new_item)

	return jsonify({'message':'Store Not Found'})



# GET /store/<string:name>/item
@app.route('/store/<string:name>/item', methods = ['GET'])
def get_item_in_store(name):

	for store in stores:
		if store['name'] == name:
			return jsonify({'items': store['items']})	
	return jsonify({'message':'Store Not Found'})


app.run(host = '127.0.0.1',
		port = 5000)