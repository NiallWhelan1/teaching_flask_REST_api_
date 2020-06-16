from werkzeug.security import safe_str_cmp ## Library for comparuing strings across string formats (e.g. ASCI to Unicode)

from user import User


users = [
	User(1, 'Jim', 'test')
]

username_mapping = {u.username: u for u in users}

userid_mapping = {u.id: u for u in users}


def authenticate(username, password):
	user = username_mapping.get(username, None)
	if user is not None and safe_str_cmp(user.password, password): ## Same as user['password'] == password for multiple character sets
		return user

def identity(payload):
	user_id = payload['identity']
	return userid_mapping.get(user_id, None)
