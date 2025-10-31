import unittest
from .image_db import session, Image, Base, engine, ImageType
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

class ImageDBTestCase(unittest.TestCase):
    def test_create_image(self):
        """通过UUID文件名获取图片"""
        # 检查数据库中是否存在且未删除
        test_file_name = '143a1547183f4e0eb8cb2869c30b549e.jpg'
        file_on_disk_name = ''
        image = session.query(Image).filter_by(
            uuid_filename=test_file_name,
            is_deleted=False
        ).first()

        if image is None:
            # 尝试通过原始文件名查找-不推荐，可能有重复
            image = session.query(Image).filter_by(
                original_filename=test_file_name,
                is_deleted=False
            ).first()
            file_on_disk_name = image.uuid_filename if image else None
        self.assertIsNotNone(image)
        self.assertIsNotNone(image.image_type)
        new_image_dict = image.to_dict()
        self.assertIsNotNone(new_image_dict)
        self.assertEqual(new_image_dict['url'], "/images/10_douban_movie/143a1547183f4e0eb8cb2869c30b549e.jpg")

# python -m unittest models/image_db_test.py
if __name__ == "__main__":
    unittest.main()

    # img = get_image('0a6429c70f89488ca5f7c0c43ae4da53.jpg')
    #
    # if img:
    #     print(img.to_dict())
    #     if img.image_type:
    #         print(f"Image type: {img.image_type.to_dict()}")
    #         type_id_type_name = f"{img.image_type.type_id}_{img.image_type.type_name}"
    #         print(type_id_type_name)
    #
    #         BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    #         UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    #         filepath = os.path.join(UPLOAD_FOLDER, type_id_type_name, img.uuid_filename)