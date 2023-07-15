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

@api_bp.errorhandler(500)
def internal_server_error(e):
    print(f"bleu print internal_server_error {e}")
    # 针对本蓝图URL空间中的500处理
    response = response_manager.json_response({'code': '500', 'message': 'The server encounter a error!'})
    return response

@api_bp.route('/search/', methods=['POST', 'GET'])
def find_movie_action():
    info = {}
    resp = response_manager.json_response(info['user'])
    return resp

@api_bp.route('/login/', methods=['POST', 'GET'])
def user_login_action():
    params = getRequestParamters(request)
    username = ''
    password = ''
    if params is not None and 'username' in params:
        username = params['username']
    if params is not None and 'password' in params:
        password = params['password']
    LoginForm(request.form)
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
