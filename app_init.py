from flask import Flask
import os

from logger.logger import get_logger
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    init_directories(app)
    return app

# 在应用初始化时创建目录
def init_directories(app):
    # 创建必要的目录
    try:
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'thumbnails'), exist_ok=True)
        print(f"✓ 目录创建成功: {app.config['UPLOAD_FOLDER']}")
    except PermissionError as e:
        print(f"✗ 权限错误: {e}")
        print(f"  请确保运行用户有权限访问: {app.config['UPLOAD_FOLDER']}")
    except Exception as e:
        print(f"✗ 创建目录失败: {e}")