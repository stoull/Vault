import os
from PIL import Image


def allowed_file(filename, allowed_extensions):
    """检查文件扩展名是否允许"""
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in allowed_extensions


def create_thumbnail(image_path, size=(300, 300)):
    """创建缩略图"""
    # 创建缩略图目录
    thumbnail_dir = os.path.join(os.path.dirname(image_path), 'thumbnails')
    os.makedirs(thumbnail_dir, exist_ok=True)

    # 生成缩略图路径
    filename = os.path.basename(image_path)
    thumbnail_path = os.path.join(thumbnail_dir, filename)

    # 创建缩略图
    with Image.open(image_path) as img:
        img.thumbnail(size, Image.Resampling.LANCZOS)
        img.save(thumbnail_path, optimize=True, quality=85)

    return thumbnail_path