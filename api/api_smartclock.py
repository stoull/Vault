import re
from flask import Flask, request, abort, Blueprint
from flask import Flask

# API with JSON
from flask import jsonify, json

from models.response_manager import ResponseManager
from models.vt_request import getRequestParamters

# 温湿度相关
from .smartclock_db_operator import readTheLastRecord, readTheLastEightHoursRecord, readRecordsWithPeriod
from .smartclock_db_operator import readHomePodRecord, insertAHomePodRecord, insertAirConditionerRecord, readAirConditionerRecord
from .smartclock_db_operator import readNoteRecord, insertNoteRecord
from .smartclock_db_operator import insert_screen_action, read_screen_actions
from .api_helper import is_date_format_valid

# 人体检测相关
from .screen_control import ScreenControl

# mqtt相关
from .smartclock_db_operator import readFridgeRecordsWithPeriod
from .mqtt_subscriber import start_listening_mqtt

smart_clock_bp = Blueprint('smart_clock', __name__)
app = Flask(__name__)
response_manager = ResponseManager(app)

# 开始mqtt的监听
start_listening_mqtt()

@smart_clock_bp.errorhandler(400)
def bad_request__error(e):
    print(f"bleu print internal_server_error {e}")
    # 针对本蓝图URL空间中的500处理
    response = response_manager.json_response({'code': '400', 'message': 'Paramters error'})
    return response

@smart_clock_bp.errorhandler(500)
def internal_server_error(e):
    print(f"bleu print internal_server_error {e}")
    # 针对本蓝图URL空间中的500处理
    response = response_manager.json_response({'code': '500', 'message': 'The server encounter a error!'})
    return response

@smart_clock_bp.route('/screen-action', methods=['GET'])
def read_screen_action_api():
    params = getRequestParamters(request)
    count = 20
    if 'count' in params:
        count = params['count']
    result_dic = read_screen_actions(count)
    response = response_manager.json_response(result_dic)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@smart_clock_bp.route('/screen-action', methods=['POST'])
def insert_screen_action_api():
    params = getRequestParamters(request)
    print(f"xxxxxx {params}")

    result_dic = {"result": 0, "message": 'falied'}
    if 'action' not in params:
        abort(400)
    else:
        action = params['action']
        insert_screen_action(action)
        result_dic = {"result": 1, "message": 'success'}
    response = response_manager.json_response(result_dic)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@smart_clock_bp.route('/note', methods=['GET'])
def read_note():
    params = getRequestParamters(request)
    count = 1
    if 'count' in params:
        count = params['count']
    result_dic = readNoteRecord(count)
    response = response_manager.json_response(result_dic)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@smart_clock_bp.route('/note', methods=['POST'])
def insert_note():
    params = getRequestParamters(request)

    if 'note' not in params:
        abort(400)
    else:
        note = params['note']
        insertNoteRecord(note)
        result_dic = {"result": 1, "message": 'success'}
    response = response_manager.json_response(result_dic)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@smart_clock_bp.route('/temperature-humidity/airconditioner', methods=['GET'])
def read_airconditioner_record():
    result_dic = readAirConditionerRecord()
    response = response_manager.json_response(result_dic)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@smart_clock_bp.route('/temperature-humidity/airconditioner', methods=['POST'])
def insert_airconditioner_record(params):
    params = getRequestParamters(request)

    location = 'HOME'
    temperature = 25
    model = '1'
    description = ''
    if params is not None:
        if 'location' in params:
            location = params['location']
        if 'temperature' in params:
            temperature = params['temperature']
        if 'model' in params:
            model = params['model']
        if 'description' in params:
            description = params['description']
        insertAirConditionerRecord([location, temperature, model, description])
        result_dic = {"result": 1, "message": 'success'}
    else:
        result_dic = {"result": 0, "message": 'fail'}
    response = response_manager.json_response(result_dic)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@smart_clock_bp.route('/control/screen', methods=['POST'])
def pi_control_screen_action():
    params = getRequestParamters(request)
    result_dic = {}
    if 'state' not in params:
        abort(400)
    else:
        state = params['state']
        if state == 'on' or state == '开' or state == 'turnOn' or state == '打开' or state == '1':
            state = ScreenControl.turn_screen_on()
        elif state == 'off' or state == '关' or state == '关闭' or state == 'turnOff' or state == '0':
            state = ScreenControl.turn_screen_off()
        result_dic = {"result": state}
    response = response_manager.json_response(result_dic)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
@smart_clock_bp.route('/control/screen', methods=['GET'])
def pi_control_screen_state():
    state = ScreenControl.current_screen_state()
    state_result = {"state": state}
    response = response_manager.json_response(state_result)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@smart_clock_bp.route('/temperature-humidity/homepod', methods=['POST'])
def insert_home_pod_record():
    params = getRequestParamters(request)
    result_dic = {"result": 0}
    if 'temp' not in params and 'humidity' not in params:
        abort(400)
    else:
        temp_str = params['temp']
        temp = float(re.sub(r'[^\d.]+', '', temp_str))
        humidity = params['humidity']
        insertAHomePodRecord([temp, humidity])
        result_dic = {"result": 1}
    response = response_manager.json_response(result_dic)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@smart_clock_bp.route('/temperature-humidity/homepod', methods=['GET'])
def read_home_pod_records():
    result_dic = readHomePodRecord()
    response = response_manager.json_response(result_dic)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# 获取温湿度
@smart_clock_bp.route('/temperature-humidity', methods=['POST', 'GET'])
def readTempAndHumidity():
    result_dic = readTheLastRecord()
    response = response_manager.json_response(result_dic)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@smart_clock_bp.route('/temperature-humidity/history', methods=['POST', 'GET'])
def readTempAndHumidityHistory():
    result_dic = readTheLastEightHoursRecord()
    response = response_manager.json_response(result_dic)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@smart_clock_bp.route('/surroundings/history', methods=['POST', 'GET'])
def readSurroundingsRecordsWithPeriod():
    params = getRequestParamters(request)
    result_dic = {}
    if 'startDate' not in params or 'endDate' not in params:
        result_dic = {'message': 'Must have startDate and endDate'}
    elif not is_date_format_valid(params['startDate']) or not is_date_format_valid(params['endDate']):
        result_dic = {'message': 'The dateformat is invalid'}
    else:
        result_dic = readRecordsWithPeriod(params['startDate'], params['endDate'])
    response = response_manager.json_response(result_dic)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@smart_clock_bp.route('/fridge/history', methods=['POST', 'GET'])
def readFridgeRecordsWithPeriod_server():
    params = getRequestParamters(request)
    result_dic = {}
    if 'startDate' not in params or 'endDate' not in params:
        result_dic = {'message': 'Must have startDate and endDate'}
    elif not is_date_format_valid(params['startDate']) or not is_date_format_valid(params['endDate']):
        result_dic = {'message': 'The dateformat is invalid'}
    else:
        result_dic = readFridgeRecordsWithPeriod(params['startDate'], params['endDate'])
    response = response_manager.json_response(result_dic)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
