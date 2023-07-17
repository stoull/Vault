from flask import jsonify, json


class ResponseManager():

    app = None

    def __init__(self, app):
        ResponseManager.app = app

    # 生成 application/json 类型的响应
    @classmethod
    def json_response(cls, dict_data):
        response = ResponseManager.app.response_class(response=json.dumps(dict_data, ensure_ascii=False),
                                                      status=200,
                                                      mimetype='application/json;charset=utf-8')
        return response
