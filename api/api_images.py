from flask import Blueprint, request, jsonify, send_from_directory, current_app
from werkzeug.utils import secure_filename
import os
import uuid
from PIL import Image as PILImage
from models.image_db import session, Image, ImageType
from sqlalchemy import func, or_, and_
from utils import allowed_file, create_thumbnail_diff_dir, calculate_fileobject_md5

from models.vt_request import get_request_parameters, get_value_from_request_params
from .api_response import ApiResponse
from .error_handlers import register_global_error_handlers

from flask import Blueprint, request, jsonify
from .exceptions import (
    ValidationException,
    ResourceNotFoundException,
    BusinessRuleException
)
from .error_codes import ErrorCodes

image_bp = Blueprint('image', __name__)

# 全局错误处理，对所有blueprint都生效
register_global_error_handlers(image_bp)

def check_image_duplicate(image_md5):
    """检查文件是否重复"""
    existing_image = session.query(Image).filter_by(md5_hash=image_md5).first()
    return existing_image or None

# 单个图片上传接口
@image_bp.route('/upload', methods=['POST'])
def upload_image():
    """上传图片并保存元数据到数据库"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    params = get_request_parameters(request)

    type_id = 0
    folder_name = '0_others'
    try:
        type_id = int(params['type_id'])
        image_type = session.query(ImageType).filter_by(
            type_id=type_id
        ).first()
        if image_type:
            folder_name = f"{image_type.type_id}_{image_type.type_name}"
    except (KeyError, ValueError, TypeError):
        if 'type_name' in params:
            type_name = params['type_name']
            image_type = session.query(ImageType).filter_by(
                type_name=type_name
            ).first()
            folder_name = '0_other'
            if image_type:
                folder_name = f"{image_type.type_id}_{image_type.type_name}"

    tags = params.get('tags') or None

    if not file or not allowed_file(file.filename, current_app.config['ALLOWED_EXTENSIONS']):
        return jsonify({'error': 'File type not allowed'}), 400

    filepath = None
    try:
        # 生成唯一文件名
        ext = os.path.splitext(secure_filename(file.filename))[1]
        uuid_filename = f"{uuid.uuid4().hex}{ext}"
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], folder_name, uuid_filename)
        thumbnail_dir = current_app.config['UPLOAD_FOLDER']
        # print(f'Generated UUID filepath: {filepath}')
        small_check_md5 = calculate_fileobject_md5(file, chunk_size=512 * 1024)

        # print(f'Calculated MD5 (first 64KB)- {file.filename} : {small_check_md5}')

        # 检查重复
        duplicate_image = check_image_duplicate(small_check_md5)
        if duplicate_image:
            return jsonify({
                'success': True,
                'message': 'Duplicate image found',
                'data': duplicate_image.to_dict()
            }), 200

        # 保存原图
        file.save(filepath)

        # 获取图片信息
        file_size = os.path.getsize(filepath)
        # small_check_md5 = calculate_partial_md5_flexible(filepath, 512 * 1024)  # 前64KB
        width, height = None, None

        try:
            with PILImage.open(filepath) as img:
                width, height = img.size
        except Exception as e:
            current_app.logger.warning(f"Cannot get image dimensions: {e}")

        # 创建缩略图
        try:
            create_thumbnail_diff_dir(filepath, thumbnail_dir, current_app.config['THUMBNAIL_SIZE'])
        except Exception as e:
            current_app.logger.error(f"Failed to create thumbnail: {e}")

        # 保存到数据库
        image = Image(
            type_id=type_id,
            tags=tags,
            uuid_filename=uuid_filename,
            original_filename=file.filename,
            file_size=file_size,
            md5_hash=small_check_md5,
            mime_type=file.content_type,
            width=width,
            height=height,
            description=request.form.get('description')  # 可选描述
        )

        session.add(image)
        session.commit()

        return jsonify({
            'success': True,
            'data': image.to_dict()
        }), 200

    except Exception as e:
        session.rollback()
        # 删除已上传的文件
        if filepath and os.path.exists(filepath):
            os.remove(filepath)
        current_app.logger.error(f"Upload failed: {e}")
        return jsonify({'error': 'Upload failed', 'message': str(e)}), 500

# 多图片上传接口
@image_bp.route('/multiple_upload', methods=['POST'])
def upload_multiple_images():
    """上传图片并保存元数据到数据库，支持单文件和多文件上传，增加文件个数及文件大小的验证处理"""
    MAX_FILES = 10  # 最大文件数，可根据需求调整
    MAX_FILE_SIZE = 15 * 1024 * 1024  # 单文件最大10MB，可根据需求调整

    files = request.files.getlist('file')
    if not files or files[0].filename == '':
        return jsonify({'error': 'No file(s) selected or filename not set'}), 400
    if len(files) > MAX_FILES:
        return jsonify({'error': f'Too many files. Maximum allowed is {MAX_FILES}.'}), 400

    params = get_request_parameters(request)
    type_id = 0
    folder_name = '0_others'
    try:
        type_id = int(params['type_id'])
        image_type = session.query(ImageType).filter_by(type_id=type_id).first()
        if image_type:
            folder_name = f"{image_type.type_id}_{image_type.type_name}"
    except (KeyError, ValueError, TypeError):
        if 'type_name' in params:
            type_name = params['type_name']
            image_type = session.query(ImageType).filter_by(type_name=type_name).first()
            folder_name = '0_other'
            if image_type:
                folder_name = f"{image_type.type_id}_{image_type.type_name}"

    tags = params.get('tags') or None
    results = []
    for file in files:
        if not file or not allowed_file(file.filename, current_app.config['ALLOWED_EXTENSIONS']):
            results.append({'filename': file.filename, 'error': 'File type not allowed'})
            continue
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        if file_size > MAX_FILE_SIZE:
            results.append({'filename': file.filename, 'error': f'File size exceeds {MAX_FILE_SIZE // (1024*1024)}MB'})
            continue
        filepath = None
        try:
            ext = os.path.splitext(secure_filename(file.filename))[1]
            uuid_filename = f"{uuid.uuid4().hex}{ext}"
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], folder_name, uuid_filename)
            thumbnail_dir = current_app.config['UPLOAD_FOLDER']
            small_check_md5 = calculate_fileobject_md5(file, chunk_size=512 * 1024)
            duplicate_image = check_image_duplicate(small_check_md5)
            if duplicate_image:
                results.append({
                    'filename': file.filename,
                    'success': True,
                    'message': 'Duplicate image found',
                    'data': duplicate_image.to_dict()
                })
                continue
            file.save(filepath)
            # file_size 已在前面获取
            width, height = None, None
            try:
                with PILImage.open(filepath) as img:
                    width, height = img.size
            except Exception as e:
                current_app.logger.warning(f"Cannot get image dimensions: {e}")
            try:
                create_thumbnail_diff_dir(filepath, thumbnail_dir, current_app.config['THUMBNAIL_SIZE'])
            except Exception as e:
                current_app.logger.error(f"Failed to create thumbnail: {e}")
            image = Image(
                type_id=type_id,
                tags=tags,
                uuid_filename=uuid_filename,
                original_filename=file.filename,
                file_size=file_size,
                md5_hash=small_check_md5,
                mime_type=file.content_type,
                width=width,
                height=height,
                description=request.form.get('description')
            )
            session.add(image)
            session.commit()
            results.append({
                'filename': file.filename,
                'success': True,
                'data': image.to_dict()
            })
        except Exception as e:
            session.rollback()
            if filepath and os.path.exists(filepath):
                os.remove(filepath)
            current_app.logger.error(f"Upload failed: {e}")
            results.append({'filename': file.filename, 'error': 'Upload failed', 'message': str(e)})
    return jsonify({'results': results}), 200

@image_bp.route('/<path:filepath>', methods=['GET'])
def get_image(filepath):
    """通过UUID文件名获取图片"""
    # 检查数据库中是否存在且未删除

    # 提取文件名
    filename = os.path.basename(filepath)
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
        return jsonify({'error': 'Image not found'}), 404

    folder_name = '0_others'
    if image.image_type:
        folder_name = f"{image.image_type.type_id}_{image.image_type.type_name}"
    file_on_disk_name = os.path.join(folder_name, file_on_disk_name)
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], file_on_disk_name)
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found on disk'}), 404

    return send_from_directory(current_app.config['UPLOAD_FOLDER'], file_on_disk_name)


@image_bp.route('/thumbnails/<filename>', methods=['GET'])
def get_thumbnail(filename):
    """获取缩略图"""
    thumbnail_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'thumbnails')
    thumbnail_path = os.path.join(thumbnail_dir, filename)

    if not os.path.exists(thumbnail_path):
        return jsonify({'error': 'Thumbnail not found'}), 404

    return send_from_directory(thumbnail_dir, filename)


@image_bp.route('/download/<int:image_id>', methods=['GET'])
def download_image(image_id):
    """下载图片，使用原始文件名"""
    image = session.query(Image).filter_by(
        id=image_id,
        is_deleted=False
    ).first()

    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], image.uuid_filename)
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found on disk'}), 404

    return send_from_directory(
        current_app.config['UPLOAD_FOLDER'],
        image.uuid_filename,
        as_attachment=True,
        download_name=image.original_filename
    )


@image_bp.route('/<int:image_id>', methods=['DELETE'])
def delete_image(image_id):
    """软删除图片"""
    image = session.query(Image).filter_by(
        id=image_id,
        is_deleted=False
    ).first()

    try:
        # 软删除（推荐）
        image.is_deleted = True
        session.commit()

        # 如果需要物理删除文件，取消下面的注释
        # filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], image.uuid_filename)
        # if os.path.exists(filepath):
        #     os.remove(filepath)
        #
        # thumbnail_path = os.path.join(
        #     current_app.config['UPLOAD_FOLDER'],
        #     'thumbnails',
        #     image.uuid_filename
        # )
        # if os.path.exists(thumbnail_path):
        #     os.remove(thumbnail_path)

        return jsonify({
            'success': True,
            'message': 'Image deleted successfully'
        }), 200

    except Exception as e:
        session.rollback()
        current_app.logger.error(f"Delete failed: {e}")
        return jsonify({'error': 'Delete failed', 'message': str(e)}), 500


@image_bp.route('/list', methods=['GET'])
def list_images():
    """列出所有图片（支持分页和筛选）"""
    try:
        # 分页参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        per_page = min(per_page, 100)  # 限制最大每页数量

        # 筛选参数
        search = request.args.get('search', '')

        # 构建查询
        query = Image.query.filter_by(is_deleted=False)

        if search:
            query = query.filter(
                or_(
                    Image.original_filename.contains(search),
                    Image.description.contains(search)
                )
            )

        # 排序并分页
        pagination = query.order_by(Image.upload_time.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

        return jsonify({
            'success': True,
            'data': {
                'images': [img.to_dict() for img in pagination.items],
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': pagination.total,
                    'pages': pagination.pages,
                    'has_next': pagination.has_next,
                    'has_prev': pagination.has_prev
                }
            }
        }), 200

    except Exception as e:
        current_app.logger.error(f"List failed: {e}")
        return jsonify({'error': 'Failed to list images', 'message': str(e)}), 500


@image_bp.route('/<int:image_id>/info', methods=['GET'])
def get_image_info(image_id):
    """获取图片详细信息"""
    image = session.query(Image).filter_by(
        id=image_id,
        is_deleted=False
    ).first()
    return jsonify({
        'success': True,
        'data': image.to_dict()
    }), 200


@image_bp.route('/<int:image_id>', methods=['PUT', 'PATCH'])
def update_image_info(image_id):
    """更新图片信息（如描述）"""
    image = session.query(Image).filter_by(
        id=image_id,
        is_deleted=False
    ).first()

    data = request.get_json()

    if 'description' in data:
        image.description = data['description']

    try:
        session.commit()
        return jsonify({
            'success': True,
            'data': image.to_dict()
        }), 200
    except Exception as e:
        session.rollback()
        return jsonify({'error': 'Update failed', 'message': str(e)}), 500


@image_bp.route('/stats', methods=['GET'])
def get_stats():
    """获取图片服务统计信息"""
    try:
        total_images = Image.query.filter_by(is_deleted=False).count()
        total_size = session.query(
            func.sum(Image.file_size)
        ).filter_by(is_deleted=False).scalar() or 0

        return jsonify({
            'success': True,
            'data': {
                'total_images': total_images,
                'total_size': total_size,
                'total_size_human': Image._format_size(total_size)
            }
        }), 200
    except Exception as e:
        return jsonify({'error': 'Failed to get stats', 'message': str(e)}), 500


# 获取图片类型列表
@image_bp.route('/types', methods=['GET'])
def get_image_types():
    """获取所有图片类型"""

    # 获取授权码
    auth_code, error = get_value_from_request_params(request, 'AuthenticationCode')
    if error:
        raise ValidationException(message="获取AuthenticationCode失败", error_code=ErrorCodes.PERMISSION_DENIED)
    if auth_code != current_app.config.get('IMAGE_SERVICE_AUTH_CODE'):
        raise ValidationException(message="获取AuthenticationCode失败", error_code=ErrorCodes.PERMISSION_DENIED)

    image_types = session.query(ImageType).all()
    types_list = [{
        'type_id': img_type.type_id,
        'type_name': img_type.type_name,
        'description': img_type.description
    } for img_type in image_types]

    return jsonify({
        'success': True,
        'data': types_list
    }), 200

@image_bp.route('/types', methods=['POST'])
def create_image_types():
    """创建新的图片类型"""
    # 获取授权码
    auth_code, error = get_value_from_request_params(request, 'AuthenticationCode')
    if error:
        raise ValidationException(message="获取AuthenticationCode失败", error_code=ErrorCodes.PERMISSION_DENIED)
    if auth_code != current_app.config.get('IMAGE_SERVICE_AUTH_CODE'):
        raise ValidationException(message="获取AuthenticationCode失败", error_code=ErrorCodes.PERMISSION_DENIED)

    data = request.get_json()
    if not data or 'type_id' not in data or 'type_name' not in data:
        return jsonify({'error': 'type_id and type_name are required'}), 400

    type_id = data['type_id']
    type_name = data['type_name']
    description = data.get('description') or ''

    existing_type = session.query(ImageType).filter(
        or_(
            ImageType.type_id == type_id,
            ImageType.type_name == type_name
        )
    ).first()
    if existing_type:
        return jsonify({'error': 'Image type with same ID or name already exists'}), 400

    try:
        new_type = ImageType(
            type_id=type_id,
            type_name=type_name,
            description=description
        )
        session.add(new_type)
        session.commit()

        return jsonify({
            'success': True,
            'data': {
                'type_id': new_type.type_id,
                'type_name': new_type.type_name,
                'description': new_type.description
            }
        }), 201

    except Exception as e:
        session.rollback()
        current_app.logger.error(f"Create image type failed: {e}")
        return jsonify({'error': 'Create image type failed', 'message': str(e)}), 500

@image_bp.route('/types/<int:type_id>', methods=['GET'])
def get_image_types_with_id(type_id):
    return f"获取 type {type_id}"

# 更新 type
@image_bp.route('/types/<int:type_id>', methods=['PUT'])
def update_image_type(type_id):
    # 获取授权码
    auth_code, error = get_value_from_request_params(request, 'AuthenticationCode')
    if error:
        raise ValidationException(message="获取AuthenticationCode失败", error_code=ErrorCodes.PERMISSION_DENIED)
    if auth_code != current_app.config.get('IMAGE_SERVICE_AUTH_CODE'):
        raise ValidationException(message="获取AuthenticationCode失败", error_code=ErrorCodes.PERMISSION_DENIED)

    return f"更新 type {type_id}"

# 删除 type
@image_bp.route('/types/<int:type_id>', methods=['DELETE'])
def delete_image_type(type_id):
    # 获取授权码
    auth_code, error = get_value_from_request_params(request, 'AuthenticationCode')
    if error:
        raise ValidationException(message="获取AuthenticationCode失败", error_code=ErrorCodes.PERMISSION_DENIED)
    if auth_code != current_app.config.get('IMAGE_SERVICE_AUTH_CODE'):
        raise ValidationException(message="获取AuthenticationCode失败", error_code=ErrorCodes.PERMISSION_DENIED)
    return f"删除 type {type_id}"
