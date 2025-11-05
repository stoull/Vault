import hashlib
import os
from PIL import Image as PILImage


def calculate_partial_md5_flexible(file_path, bytes_to_read=64 * 1024):
    """计算文件前指定字节数的 MD5"""
    hash_md5 = hashlib.md5()

    with open(file_path, "rb") as f:
        # 读取指定字节数
        data = f.read(bytes_to_read)
        hash_md5.update(data)

    return hash_md5.hexdigest()

# 不同大小的测试
# small_check = calculate_partial_md5_flexible("image.jpg", 64 * 1024)  # 前64KB
# medium_check = calculate_partial_md5_flexible("image.jpg", 512 * 1024)  # 前512KB
# large_check = calculate_partial_md5_flexible("image.jpg", 1024 * 1024)  # 前1MB

def calculate_partial_md5_chunked(file_path, total_bytes=64 * 1024, chunk_size=4096):
    """分块读取文件前部分内容计算 MD5"""
    hash_md5 = hashlib.md5()
    bytes_read = 0

    with open(file_path, "rb") as f:
        while bytes_read < total_bytes:
            # 计算本次读取的字节数
            bytes_to_read = min(chunk_size, total_bytes - bytes_read)
            chunk = f.read(bytes_to_read)

            if not chunk:  # 文件结束
                break

            hash_md5.update(chunk)
            bytes_read += len(chunk)

    return hash_md5.hexdigest(), bytes_read

# 不同大小的测试
# small_check = calculate_partial_md5_chunked("image.jpg", 64 * 1024)  # 前64KB
# medium_check = calculate_partial_md5_chunked("image.jpg", 512 * 1024)  # 前512KB
# large_check = calculate_partial_md5_chunked("image.jpg", 1024 * 1024)  # 前1MB

def calculate_fileobject_md5(file_object, chunk_size=64 * 1024):
    """
    计算文件对象前64KB的MD5值
    Args:
        file_object: Flask request.files 中的文件对象
        chunk_size: 读取的字节数，默认 64KB (65536 bytes)

    Returns:
        str: MD5哈希值（十六进制字符串）
    """
    # 保存当前文件指针位置
    current_position = file_object.tell()
    # 移动到文件开头
    file_object.seek(0)
    # 创建MD5对象
    md5_hash = hashlib.md5()
    # 只读取前64KB
    chunk = file_object.read(chunk_size)
    md5_hash.update(chunk)
    # 恢复文件指针到原来的位置（重要！）
    file_object.seek(current_position)
    return md5_hash.hexdigest()

def allowed_file(filename, allowed_extensions):
    """检查文件扩展名是否允许"""
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in allowed_extensions

# 在原始目录下创建缩略图
def create_thumbnail(image_path, size=(300, 300)):
    """创建缩略图"""
    # 创建缩略图目录
    thumbnail_dir = os.path.join(os.path.dirname(image_path), 'thumbnails')
    os.makedirs(thumbnail_dir, exist_ok=True)

    # 生成缩略图路径
    filename = os.path.basename(image_path)
    thumbnail_path = os.path.join(thumbnail_dir, filename)
    print(f"Creating thumbnail at: {thumbnail_path}")

    # 创建缩略图
    with PILImage.open(image_path) as img:
        img.thumbnail(size, PILImage.Resampling.LANCZOS)
        img.save(thumbnail_path, optimize=True, quality=85)

    return thumbnail_path

# 指定目标目录创建缩略图
def create_thumbnail_diff_dir(image_path, thumbnail_dir, size=(300, 300)):
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