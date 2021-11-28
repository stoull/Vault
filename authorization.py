
class AuthManager():
	"""docstring for AuthManager"""
	def __init__(self):
		authenticated_user_list = []

	def isAuthenticated(self, username):
		if username in authenticated_user_list:
			return True
		else:
			return False

	def authorize(self, login_form):
		# if login_form.username is exist: and password is right
		if login_form.password == '123':
			authenticated_user_list.append(username)
			return True
		else:
			return False

	def deAuthorize(self, username):
		authenticated_user_list.remove(username)

		