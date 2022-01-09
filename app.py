import sqlite3
from flask import Flask, request, Response, render_template
from jinja2 import Environment, PackageLoader
from markupsafe import escape
from flask import make_response
from flask import session
from flask import Flask,redirect

# a if condition else b

from models.form import LoginForm
from models.authorization import AuthManager

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
			# 登录成功

			# 重定向
			resp = make_response(redirect(f"/user/{login_form.username}"))
			resp.set_cookie("username", login_form.username)
			return resp

			# 返回静态页,url不变
			# resp = make_response(render_template('home.html', user_name=login_form.username))
			# resp.set_cookie("username", login_form.username)
			# return resp
		else:
			return render_template('login.html', error_password=True)
	else:
		return render_template('login.html', error_password=True)
	# template = env.get_template('login.html')
	# return template.render()

@app.route("/logout", methods=['GET'])
def logout():
	cookied_username = request.cookies.get('username')
	if cookied_username is not None and auth_manager.isAuthenticated(cookied_username):
		resp = make_response(render_template('login.html', error_password=False))
		resp.set_cookie("username", "", expires=0)
		return resp
	else:
		return render_template('login.html', error_password=False)

@app.route("/")
@app.route("/index")
def index_page():
	# 静态页
	# return app.send_static_file('login.html')
	cookied_username = request.cookies.get('username')
	if cookied_username is not None and auth_manager.isAuthenticated(cookied_username):
		return render_template('index.html', user_name=escape(cookied_username))
	else:
		return render_template('index.html')

	# template = env.get_template('index.html')
	# return template.render()

@app.route("/user/<username>")
def home_page(username):
	authResult = checkUserAuthentication(username)
	if authResult == True:
		return render_template('home.html', user_name=escape(username))
	else:
		return authResult

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



# 如已授权则返回true, 未授权则返返回登录界面的重定向
def checkUserAuthentication(username):
	if auth_manager.isAuthenticated(username):
		return True
	else:
		# 重定向到登录界面
		resp = make_response(redirect(f"/login"))
		return resp



@app.route("/backstage", methods=['GET'])
def backstage():
	cookied_username = request.cookies.get('username')
	if cookied_username is not None and auth_manager.isAuthenticated(cookied_username):
		return render_template('backstage.html', user_name=escape(cookied_username))
	else:
		return make_response(redirect(f"/login"))

@app.route("/movie/<movieName>", methods=['GET'])
def moviePage(movieName):
	cookied_username = request.cookies.get('username')
	if cookied_username is not None and auth_manager.isAuthenticated(cookied_username):
		return render_template('movie.html', movie_name=escape(movieName))
	else:
		return make_response(redirect(f"/login"))

# API with JSON
from flask import jsonify
@app.route("/json/tables/", methods=['GET'])
def get_database_tables():
	con = sqlite3.connect('models/vault.db')
	cur = con.cursor()
	cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
	tables_names = []
	for tableName in cur.fetchall():
		tables_names.append(tableName[0])
	con.commit()
	cur.close()
	return jsonify(tables_names)
	# return Response(json.dumps(talbe_names), mimetype='application/json')

@app.route("/json/content/<tableName>", methods=['GET'])
def get_database_data(tableName):
	con = sqlite3.connect('models/vault.db')
	cur = con.cursor()
	if tableName == "user":
		cur.execute("SELECT * FROM user LIMIT 10")
	elif tableName == "movie":
		cur.execute("SELECT * FROM movie LIMIT 10")
	elif tableName == "director":
		cur.execute("SELECT * FROM director LIMIT 10")
	if tableName == "actor":
		cur.execute("SELECT * FROM actor LIMIT 10")
	elif tableName == "scenarist":
		cur.execute("SELECT * FROM scenarist LIMIT 10")
	elif tableName == "area":
		cur.execute("SELECT * FROM area LIMIT 10")
	elif tableName == "type":
		cur.execute("SELECT * FROM type LIMIT 10")
	if tableName == "tag":
		cur.execute("SELECT * FROM tag LIMIT 10")
	else:
		pass
	datas = []
	for data in cur.fetchall():
		datas.append(data)
	con.commit()
	cur.close()
	return jsonify(datas)


