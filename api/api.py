import sqlite3
import werkzeug
from flask import Flask, request, Response, render_template
from flask import session
from flask import Flask, redirect

# API with JSON
from flask import jsonify, json

from models.form import LoginForm
from models.authorization import AuthManager
from models.response_manager import ResponseManager
from models.vt_request import getRequestParamters

from flask import Blueprint

api_bp = Blueprint('api', __name__)

app = Flask(__name__)
auth_manager = AuthManager()
response_manager = ResponseManager(app)

@app.errorhandler(werkzeug.exceptions.BadRequest)
def handle_bad_request(e):
    print(f"Blueprint api handle_bad_request: {e}")
    return render_template('page_not_found.html'), 404

@api_bp.route('/find_movie/', methods=['POST', 'GET'])
def find_movie_action():
    info = {}
    resp = response_manager.json_response(info['user'])
    return resp

@api_bp.route('/login/', methods=['POST', 'GET'])
def user_login_action():
    # application/x-www-form-urlencoded
    # form_content = request.form
    # print(f"form {form_content}")

    # json_content = request.get_json(silent=True)

    params = getRequestParamters(request)
    print(f"getRequestParamters: {params}")

    # application/json
    # json_content = request.json
    username = ''
    password = ''
    if params is not None and 'username' in params:
        username = params['username']

    if  params is not None and 'password' in params:
        password = params['password']

    LoginForm(request.form)

    print(f"username {username} pwd: {password}")

    if password == "123456":
        # 登录成功
        data = {"username": "user.username", "password": "ddddd"}
        resp = response_manager.json_response(data)

        session["name"] = "Hut_test"
        session["account_id"] = "siehdashww"

        resp.set_cookie("username", "yourusernameherecookie")
        return resp
    else:
        return jsonify(result="notlogin")
