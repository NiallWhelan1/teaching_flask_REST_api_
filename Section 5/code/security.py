from werkzeug.security import safe_str_cmp ## Library for comparuing strings across string formats (e.g. ASCI to Unicode)

from user import User

def authenticate(username, password):
	user = User.find_by_username(username)
	if user is not None and safe_str_cmp(user.password, password): ## Same as user['password'] == password for multiple character sets
		return user

def identity(payload):
	user_id = payload['identity']
	return User.find_by_id(user_id)
