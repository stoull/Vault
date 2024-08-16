import sqlite3, re
import werkzeug
from flask import Flask, request, Response, render_template, abort
from flask import session
from flask import Flask, redirect

# API with JSON
from flask import jsonify, json

from models.form import LoginForm
from models.authorization import AuthManager
from models.response_manager import ResponseManager
from models.vt_request import getRequestParamters

# 温湿度相关
from .surroundings_reader import readTheLastRecord, readTheLastEightHoursRecord, readHomePodRecord, insertAHomePodRecord

from flask import Blueprint

api_bp = Blueprint('api', __name__)

app = Flask(__name__)
auth_manager = AuthManager()
response_manager = ResponseManager(app)

@api_bp.errorhandler(400)
def bad_request__error(e):
    print(f"bleu print internal_server_error {e}")
    # 针对本蓝图URL空间中的500处理
    response = response_manager.json_response({'code': '400', 'message': 'Paramters error'})
    return response

@api_bp.errorhandler(500)
def internal_server_error(e):
    print(f"bleu print internal_server_error {e}")
    # 针对本蓝图URL空间中的500处理
    response = response_manager.json_response({'code': '500', 'message': 'The server encounter a error!'})
    return response

@api_bp.route('/temperature-humidity/homepod', methods=['POST'])
def insert_home_pod_record():
    params = getRequestParamters(request)
    temp = -999
    humidity = -999
    if params is not None and 'temp' in params:
        temp_str = params['temp']
        temperature_str = '27.3°C'
        temp = float(re.sub(r'[^\d.]+', '', temp_str))
    if params is not None and 'humidity' in params:
        humidity = params['humidity']

    result_dic = {"result": 1}
    if temp > -60 and humidity > -60:
        insertAHomePodRecord([temp, humidity])
    else:
        result_dic = {"result": 0}
    response = response_manager.json_response(result_dic)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@api_bp.route('/temperature-humidity/homepod-records', methods=['GET'])
def read_home_pod_records():
    result_dic = readHomePodRecord()
    response = response_manager.json_response(result_dic)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# 获取温湿度
@api_bp.route('/temperature-humidity', methods=['POST', 'GET'])
def readTempAndHumidity():
    result_dic = readTheLastRecord()
    response = response_manager.json_response(result_dic)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@api_bp.route('/temperature-humidity/history', methods=['POST', 'GET'])
def readTempAndHumidityHistory():
    result_dic = readTheLastEightHoursRecord()
    response = response_manager.json_response(result_dic)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@api_bp.route('/movies/search', methods=['GET'])
def search_movie():
    params = getRequestParamters(request)
    if 'keywords' not in params:
        abort(400)

    keywords = params['keywords']

    con = sqlite3.connect('models/vault.db')
    cur = con.cursor()
    cur.execute('''SELECT * FROM movie WHERE name LIKE ? ORDER BY create_date DESC LIMIT 50''', ('%'+keywords+'%',))
    datas = []
    for data in cur.fetchall():
        keyList = ["id", "name", "directors", "scenarists", "actors", "style", "year", "release_date", "area",
                   "language", "length", "other_names", "score", "rating_number", "synopsis", "imdb", "poster_name",
                   "filePath", "fileUrl", "is_downloaded", "download_link", "create_date", "lastWatch_date",
                   "lastWatch_user"]
        movieDic = {}
        for i in range(0, len(keyList)):
            key = keyList[i]
            movieDic[key] = data[i]
        if len(movieDic) > 0:
            datas.append(movieDic)
    con.commit()
    cur.close()
    resp = response_manager.json_response(datas)
    return resp

@api_bp.route('/movies', methods=['POST'])
def save_movie():
    response = response_manager.json_response({'cmd': 'post', 'message': 'You use POST'})
    return response

@api_bp.route('/movies', methods=['GET'])
def get_movie():
    response = response_manager.json_response({'code': 'get', 'message': 'You use GET'})
    return response

@api_bp.route('/login/', methods=['POST', 'GET'])
def user_login():
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
