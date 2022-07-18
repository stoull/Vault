
from models.singleton import Singleton


class AuthManager(metaclass=Singleton):
	"""docstring for AuthManager"""
	def __init__(self):
		self.authenticated_user_list = []

	def isAuthenticated(self, username):
		if username in self.authenticated_user_list:
			return True
		else:
			return False

	def authorize(self, login_form):
		# if login_form.username is exist: and password is right
		if login_form.password == '123':
			self.authenticated_user_list.append(login_form.username)
			return True
		else:
			return False

	def deAuthorize(self, username):
		self.authenticated_user_list.remove(login_form.username)

		