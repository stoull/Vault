from PIL import Image as PILImage
from image_db import session, Image, Base, engine, ImageType
import os
from werkzeug.utils import secure_filename
import uuid
import hashlib


def get_image(filename):
    """通过UUID文件名获取图片"""
    # 检查数据库中是否存在且未删除
    file_on_disk_name = filename
    image = session.query(Image).filter_by(
        uuid_filename=filename,
        is_deleted=False
    ).first()

    if image is None:
        # 尝试通过原始文件名查找-不推荐，可能有重复
        image = session.query(Image).filter_by(
            original_filename=filename,
            is_deleted=False
        ).first()
        file_on_disk_name = image.uuid_filename if image else None

    if not image:
        print("Image not found filename:", filename)
        return None
    if not image.image_type:
        print("No image type associated")
    return image

if __name__ == "__main__":
    img = get_image('0a6429c70f89488ca5f7c0c43ae4da53.jpg')

    if img:
        print(img.to_dict())
        if img.image_type:
            print(f"Image type: {img.image_type.to_dict()}")
            type_id_type_name = f"{img.image_type.type_id}_{img.image_type.type_name}"
            print(type_id_type_name)

            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
            filepath = os.path.join(UPLOAD_FOLDER, type_id_type_name, img.uuid_filename)