import os

class Config:
    # 基础配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or b'22895da8a3c21329600df4b32aa7969a1156b05c845e63ba5ad68311a5324ab5'

    # 数据库配置 - SQLite
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              f'sqlite:///{os.path.join(BASE_DIR, "image_service.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 上传配置
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 限制上传文件大小为 16MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp'}

    # 图片服务配置
    IMAGE_URL_PREFIX = '/images'
    THUMBNAIL_SIZE = (300, 300)