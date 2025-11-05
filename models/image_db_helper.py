from PIL import Image as PILImage
from .image_db import session, Image, Base, engine, ImageType
import os, shutil
from werkzeug.utils import secure_filename
import uuid
import hashlib

class ImageDBHelper:
    @staticmethod
    def check_image_duplicate(image_md5):
        """检查文件是否重复"""
        existing_image = session.query(Image).filter_by(md5_hash=image_md5).first()
        return existing_image or None

    # 录创建缩略图-指定目标目
    @staticmethod
    def create_thumbnail(image_path, thumbnail_dir, size=(300, 300)):
        """创建缩略图在本目录"""
        # 创建缩略图目录
        """
        thumbnail_dir = os.path.join(os.path.dirname(image_path), 'thumbnails')
        os.makedirs(thumbnail_dir, exist_ok=True)

        # 生成缩略图路径
        filename = os.path.basename(image_path)
        thumbnail_path = os.path.join(thumbnail_dir, filename)
        """

        """创建缩略图在目标目录"""
        thumbnail_dir = os.path.join(thumbnail_dir, 'thumbnails')
        os.makedirs(thumbnail_dir, exist_ok=True)
        filename = os.path.basename(image_path)
        thumbnail_path = os.path.join(thumbnail_dir, filename)

        # 创建缩略图
        with PILImage.open(image_path) as img:
            img.thumbnail(size, PILImage.Resampling.LANCZOS)
            try:
                img.save(thumbnail_path, optimize=True, quality=85)
                print(f"创建缩略图成功: {thumbnail_path}")
            except Exception as e:
                print(f"创建缩略图时出错: {e}")
                return False
        return thumbnail_path