import sqlite3

from flask import Flask, request, Response, render_template
from jinja2 import Environment, PackageLoader
from markupsafe import escape
from flask import make_response
from flask import session
from flask import Flask, redirect

# a if condition else b

from models.form import LoginForm
from models.authorization import AuthManager
from models.response_manager import ResponseManager

app = Flask(__name__)
app.secret_key = b'22895da8a3c21329600df4b32aa7969a1156b05c845e63ba5ad68311a5324ab5'
env = Environment(loader=PackageLoader('app', 'templates'))
auth_manager = AuthManager()
response_manager = ResponseManager(app)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

@app.route("/login", methods=['GET','POST'])
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
		return render_template('index_new.html', user_name=escape(cookied_username))
	else:
		return render_template('index_new.html')

	# template = env.get_template('index.html')
	# return template.render()

@app.route("/user/<username>")
def home_page(username):
	authResult = checkUserAuthentication(username)
	if authResult == True:
		return render_template('home.html', user_name=escape(username))
	else:
		return authResult


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

# 按movie id 查询详情信息
@app.route("/subject/<movie_id>", methods=['GET'])
def subjectDetailPage(movie_id):
	cookied_username = request.cookies.get('username')
	if cookied_username is not None and auth_manager.isAuthenticated(cookied_username):
		return render_template('movie.html', movie_id=escape(movie_id))
	else:
		return make_response(redirect(f"/login"))

@app.route("/videoPlayer/<movie_id>", methods=['GET'])
def videoPlayer(movie_id):
	cookied_username = request.cookies.get('username')
	if cookied_username is not None and auth_manager.isAuthenticated(cookied_username):
		return render_template('video_player.html', movie_id=escape(movie_id))
	else:
		return make_response(redirect(f"/login"))

# 按celebrity id 查询人物详情数据
@app.route("/celebrity/<celebrity_id>", methods=['GET'])
def celebrityDetailPage(celebrity_id):
	cookied_username = request.cookies.get('username')
	if cookied_username is not None and auth_manager.isAuthenticated(cookied_username):
		return render_template('celebrity.html', celebrity_id=escape(celebrity_id))
	else:
		return make_response(redirect(f"/login"))

# 按type id 查询分类 分类
@app.route("/category/<type_id>", methods=['GET'])
def categoryDetailPage(type_id):
	cookied_username = request.cookies.get('username')
	if cookied_username is not None and auth_manager.isAuthenticated(cookied_username):
		return render_template('celebrity.html', type_id=escape(type_id))
	else:
		return make_response(redirect(f"/login"))

# 按area id 查询地区分类
@app.route("/area/<area_id>", methods=['GET'])
def areaDetailPage(area_id):
	cookied_username = request.cookies.get('username')
	if cookied_username is not None and auth_manager.isAuthenticated(cookied_username):
		return render_template('celebrity.html', area_id=escape(area_id))
	else:
		return make_response(redirect(f"/login"))

# API with JSON
from flask import jsonify, json

@app.route("/json/subject/<subject_id>", methods=['POST'])
def get_database_movie(subject_id):
	con = sqlite3.connect('models/vault.db')
	cur = con.cursor()
	cur.execute('''SELECT * FROM movie WHERE id=? LIMIT 1''', (subject_id,))
	data = cur.fetchone()
	keyList = ["id", "name", "directors", "scenarists", "actors", "style", "year", "release_date", "area", "language",
			   "length", "other_names", "score", "rating_number", "synopsis", "imdb", "poster_name", "filePath",
			   "fileUrl", "is_downloaded", "download_link", "create_date", "lastWatch_date", "lastWatch_user"]
	movieDic = {}
	for i in range(0, len(keyList)):
		key = keyList[i]
		movieDic[key] = data[i]

	directors = []
	scenarists = []
	actors = []
	style = []
	area = []

	for row in cur.execute('''SELECT c.id, c.name  FROM movie m
	JOIN movie_actor ma ON ma.movie_id = m.id
	JOIN celebrity c ON c.id = ma.actor_id
	WHERE m.id=?;''', (subject_id,)) :
		actors.append({"id": row[0], "name": row[1]})

	for row in cur.execute('''SELECT c.id, c.name  FROM movie m
	JOIN movie_director md ON md.movie_id = m.id
	JOIN celebrity c ON c.id = md.director_id
	WHERE m.id=?;''', (subject_id,)) :
		directors.append({"id": row[0], "name": row[1]})

	for row in cur.execute('''SELECT c.id, c.name  FROM movie m
	JOIN movie_scenarist ms ON ms.movie_id = m.id
	JOIN celebrity c ON c.id = ms.scenarist_id
	WHERE m.id=?;''', (subject_id,)) :
		scenarists.append({"id": row[0], "name": row[1]})

	for row in cur.execute('''SELECT c.id, c.name  FROM movie m
	JOIN movie_type ma ON ma.movie_id = m.id
	JOIN type c ON c.id = ma.type_id
	WHERE m.id=?;''', (subject_id,)) :
		style.append({"id": row[0], "name": row[1]})

	for row in cur.execute('''SELECT c.id, c.name  FROM movie m
	JOIN movie_area ma ON ma.movie_id = m.id
	JOIN area c ON c.id = ma.area_id
	WHERE m.id=?;''', (subject_id,)) :
		area.append({"id": row[0], "name": row[1]})

	movieDic['directors'] = directors
	movieDic['scenarists'] = scenarists
	movieDic['actors'] = actors
	movieDic['style'] = style
	movieDic['area'] = area

	con.commit()
	cur.close()
	return jsonify(movieDic)

@app.route("/json/celebrity/<celebrity_id>", methods=['POST'])
def get_database_celebrity_detail(celebrity_id):
	con = sqlite3.connect('models/vault.db')
	cur = con.cursor()
	cur.execute('''SELECT * FROM celebrity WHERE id=? LIMIT 1''', (celebrity_id,))
	data = cur.fetchone()
	keyList = ["id", "name", "gender", "zodiac", "living_time", "birthday", "left_day", "birthplace", "occupation", "is_director",
			   "is_scenarist", "is_actor", "names_cn", "names_en", "family", "imdb", "intro", "portrait_name",
			   "create_date"]
	celebrityDic = {}
	for i in range(0, len(keyList)):
		key = keyList[i]
		celebrityDic[key] = data[i]
	con.commit()
	cur.close()
	return jsonify(celebrityDic)

@app.route("/json/tables/", methods=['POST'])
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

# 按表各取数据
@app.route("/json/content/<tableName>", methods=['POST'])
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

# 获取最近更新的二十个电影
@app.route("/json/movie/theLastMovies", methods=['POST'])
def get_theLastMovies():
	con = sqlite3.connect('models/vault.db')
	cur = con.cursor()
	cur.execute("SELECT * FROM movie ORDER BY create_date DESC LIMIT 20 OFFSET 0;")
	datas = []
	for data in cur.fetchall():
		keyList = ["id", "name", "directors", "scenarists", "actors", "style", "year", "release_date", "area", "language", "length", "other_names", "score", "rating_number", "synopsis", "imdb", "poster_name", "filePath", "fileUrl", "is_downloaded", "download_link", "create_date", "lastWatch_date", "lastWatch_user"]
		movieDic = {}
		for i in range(0, len(keyList)):
			key = keyList[i]
			movieDic[key] = data[i]
		if len(movieDic) > 0:
			datas.append(movieDic)
	con.commit()
	cur.close()
	return jsonify(datas)

@app.route("/loginUser", methods=['POST'])
def user_login_action():
	# application/x-www-form-urlencoded
	# form_content = request.form
	# print(f"form {form_content}")

	# json_content = request.get_json(silent=True)

	# application/json
	json_content = request.json

	username = json_content['username']
	password = json_content['password']
	LoginForm(request.form)
	if password == "123456":
		# 登录成功
		data = {"username": "user.username", "password": "ddddd"}
		resp = response_manager.json_response(data)

		session["name"] = "Hut_test"
		session["account_id"] = "siehdashww"

		resp.set_cookie("username", "yourusernameherecookie")
		return  resp
	else:
		return jsonify(result="notlogin")
