
class User:
	"""docstring for User"""
	def __init__(self, userDic):
		self.userDic = userDic
		self.username = userDic.get('username', None)
		self.password = userDic.get('password', None)
		self.email = userDic.get('email', None)
		self.is_authenticated = userDic.get('is_authenticated', False)
		self.is_active = userDic.get('is_active', False)
		self.is_anonymous = userDic.get('is_anonymous', True)

	def get_id():
		return "1234567"