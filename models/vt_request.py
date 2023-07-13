from flask import jsonify, json, request

def getRequestParamters(req):
    print(f"request.content_type: {request.content_type}")
    data = {}
    if request.content_type is None:
        if request.args is not None:
            data = request.args.to_dict()
        return data
    elif (request.content_type.startswith('application/json')):
        data = request.get_data()
        return json.loads(data.decode("utf-8"))
    elif (request.content_type.startswith("application/x-www-form-urlencoded")):
        if request.args is not None:
            data = request.args.to_dict()
        return data
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
