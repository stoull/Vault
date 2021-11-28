from user import User

class LoginForm():
	"""docstring for LoginForm"""
	def __init__(self, form):
		self.form = form
		self.username = form.get("email", None)
		self.email = form.get("email", None)
		self.password = form.get("password", None)

		is_authenticated = self.password == "123456"
		userInfo = {"username":self.username, "password":self.password, "email":self.email, "is_authenticated":is_authenticated, "is_active":False, "is_anonymous":True}
		self.user = User(userInfo)

	def validate_on_submit(self):
		if len(self.username) > 6 and len(self.password) > 3:
			return True
		else:
			return False