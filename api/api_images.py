from  flask import Flask, send_file, request, abort
import os

from flask import Blueprint

from models.vt_request import getRequestParamters
from models.response_manager import ResponseManager

app = Flask(__name__)
response_manager = ResponseManager(app)

image_bp = Blueprint('images', __name__)

@image_bp.errorhandler(400)
def bad_request__error(e):
    print(f"bleu print internal_server_error {e}")
    # 针对本蓝图URL空间中的500处理
    response = response_manager.json_response({'code': '400', 'message': 'Paramters error'})
    return response

@image_bp.errorhandler(500)
def internal_server_error(e):
    print(f"bleu print internal_server_error {e}")
    # 针对本蓝图URL空间中的500处理
    response = response_manager.json_response({'code': '500', 'message': 'The server encounter a error!'})
    return response

@image_bp.route('/poster/<image_name>', methods=['GET'])
def images_poster(image_name):
    img_dir = "./static/images/poster"
    if image_name is None:
        params = getRequestParamters(request)
        if 'id' not in params:
            abort(400)
        image_name = params['id'] + ".jpg"

    img_path = os.path.join(img_dir, image_name)
    if os.path.isfile(img_path):
        return send_file(img_path, mimetype='image/jpg')
    return response_manager.json_response({'code': '500', 'message': 'Image is not exist!'})

