from flask import jsonify, json, request

import urllib

def getRequestParamters(req):
    print(f"request.content_type: {request.content_type}")
    data = {}
    if (request.content_type.startswith('application/json')):
        data = request.get_data()
        return json.loads(data.decode("utf-8"))
    elif (request.content_type.startswith("application/x-www-form-urlencoded")):
        # print(1)
        # print(urllib.parse.parse_qs(request.get_data().decode("utf-8")))
        # return parse_qs_plus(urllib.parse.parse_qs(request.get_data().decode("utf-8")))
        return urllib.parse.parse_qs(request.get_data().decode("utf-8"))
    else:
        for key, value in request.form.items():
            if key.endswith('[]'):
                data[key[:-2]] = request.form.getlist(key)
            else:
                data[key] = value
        return data


class VaultRequest():
    def __init__(self, req):
        self.req = req

    def requestParameters(self):
        return {"username": "user.username", "password": "ddddd"}
