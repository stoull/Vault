from flask import Flask, request, render_template
from jinja2 import Environment, PackageLoader
from markupsafe import escape
from flask import make_response
from flask import session


from form import LoginForm
from authorization import AuthManager

app = Flask(__name__)
app.secret_key = b'22895da8a3c21329600df4b32aa7969a1156b05c845e63ba5ad68311a5324ab5'
env = Environment(loader=PackageLoader('app', 'templates'))
auth_manager = AuthManager()

@app.route("/login", methods=['GET', 'POST'])
def login_page():
	if request.method == 'GET':
		cookied_username = request.cookies.get('username')
		if cookied_username is not None and auth_manager.isAuthenticated(cookied_username):
			return render_template('home.html', user_name=escape(cookied_username))
		else:
			return render_template('login.html', error_password=False)
		
	elif request.method == 'POST':
		login_form = LoginForm(request.form)
		if login_form.validate_on_submit() and auth_manager.authorize(login_form):
			resp = make_response(render_template('home.html', user_name=login_form.username))
			resp.set_cookie(login_form.username, login_form.username)
			return resp
		else:
			return render_template('login.html', error_password=True)
	else:
		return render_template('login.html', error_password=True)
	# template = env.get_template('login.html')
	# return template.render()

@app.route("/")
@app.route("/index")
def index_page():
	# 静态页
	# return app.send_static_file('login.html')
	return render_template('index.html')

	# template = env.get_template('index.html')
	# return template.render()

@app.route("/user/<username>")
def home_page(username):
	return render_template('home.html', user_name=escape(username))

	# template = env.get_template('home.html')
	# return template.render(user_name=username)

@app.route("/user_login_action", methods=['POST'])
def user_login_action():
	password = request.form['password']
	email = request.form['email']
	if password == '123456':
		pass


	# env = Environment(loader=PackageLoader('app', 'templates'))

	# template = env.get_template('index.html')

	# return template.render(user_name=text)