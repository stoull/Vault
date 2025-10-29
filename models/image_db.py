from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from sqlalchemy import inspect, func, text

# 创建数据库引擎
database_url = "sqlite:///./models/images.db"
engine = create_engine(database_url, echo=True)

# 创建Session
Session = sessionmaker(bind=engine)
session = Session()

# 创建基础模型类
Base = declarative_base()

# 定义系统字典表模型
class SystemDict(Base):
    __tablename__ = "system_dict"

    id = Column(Integer, primary_key=True, autoincrement=True)
    table_name = Column(String(255), nullable=False)    # -- 表名
    column_name = Column(String(255), nullable=False)   # -- 字段名
    value = Column(String(255), nullable=False)     # -- 字段值
    meaning = Column(String(255), nullable=False)   # -- 字段含义
    description = Column(String(255), nullable=False)   # -- 字段描述
    is_active = Column(Boolean, default=True)    # -- 是否启用
    created_by = Column(String(100), nullable=False)    # -- 创建人
    created_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)    # -- 创建时间

    def __repr__(self):
        return f'<SystemDict {self.key}>'

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(Integer)  # 图片类型，预留字段
    uuid_filename = Column(String(100), unique=True, nullable=False, index=True)
    original_filename = Column(String(255), nullable=False)
    file_size = Column(Integer)
    md5_hash = Column(String(32), index=True)
    width = Column(Integer)  # 图片宽度
    height = Column(Integer)  # 图片高度
    mime_type = Column(String(50))
    user_id = Column(Integer)
    upload_time = Column(DateTime, default=datetime.now)
    created_at = Column(DateTime, default=datetime.now)  # 插入时设置
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    description = Column(Text)  # 可选：图片描述
    is_deleted = Column(Boolean, default=False)  # 软删除标记
    tags = Column(String(255))  # 可选：标签，逗号分隔

    def __repr__(self):
        return f'<Image {self.uuid_filename}>'

    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'tags': self.tags,
            'filename': self.uuid_filename,
            'original_name': self.original_filename,
            'url': f"/images/{self.uuid_filename}",
            'thumbnail_url': f"/images/thumbnails/{self.uuid_filename}",
            'size': self.file_size,
            'md5_hash': self.md5_hash,
            'size_human': self._format_size(self.file_size),
            'mime_type': self.mime_type,
            'dimensions': {
                'width': self.width,
                'height': self.height
            } if self.width and self.height else None,
            'description': self.description,
            'upload_time': self.upload_time.isoformat()
        }

    @staticmethod
    def _format_size(size_bytes):
        """格式化文件大小"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"

    @classmethod
    def get_database_status(cls):
        """获取数据库状态信息"""
        try:
            # 基础统计
            total_count = session.query(func.count(cls.id)).scalar() or 0
            active_count = session.query(func.count(cls.id)).filter_by(is_deleted=False).scalar() or 0
            deleted_count = session.query(func.count(cls.id)).filter_by(is_deleted=True).scalar() or 0

            # 存储统计
            total_size = session.query(func.sum(cls.file_size)).filter_by(is_deleted=False).scalar() or 0
            deleted_size = session.query(func.sum(cls.file_size)).filter_by(is_deleted=True).scalar() or 0

            # 文件类型统计
            mime_stats = session.query(
                cls.mime_type,
                func.count(cls.id).label('count')
            ).filter_by(is_deleted=False).group_by(cls.mime_type).all()

            # 最近上传
            latest_upload = session.query(cls).filter_by(is_deleted=False).order_by(cls.upload_time.desc()).first()
            oldest_upload = session.query(cls).filter_by(is_deleted=False).order_by(cls.upload_time.asc()).first()

            return {
                'total_images': total_count,
                'active_images': active_count,
                'deleted_images': deleted_count,
                'storage': {
                    'total_size': total_size,
                    'total_size_human': cls._format_size(total_size),
                    'deleted_size': deleted_size,
                    'deleted_size_human': cls._format_size(deleted_size)
                },
                'mime_types': {mime: count for mime, count in mime_stats},
                'latest_upload': latest_upload.upload_time.isoformat() if latest_upload else None,
                'oldest_upload': oldest_upload.upload_time.isoformat() if oldest_upload else None
            }
        except Exception as e:
            return {
                'error': str(e),
                'status': 'error'
            }

    @classmethod
    def get_table_info(cls):
        """获取表结构信息"""
        try:
            inspector = inspect(engine)
            columns = inspector.get_columns(cls.__tablename__)
            indexes = inspector.get_indexes(cls.__tablename__)

            return {
                'table_name': cls.__tablename__,
                'columns': [
                    {
                        'name': col['name'],
                        'type': str(col['type']),
                        'nullable': col['nullable'],
                        'default': str(col['default']) if col['default'] else None,
                        'primary_key': col.get('primary_key', False)
                    }
                    for col in columns
                ],
                'indexes': [
                    {
                        'name': idx['name'],
                        'columns': idx['column_names'],
                        'unique': idx['unique']
                    }
                    for idx in indexes
                ]
            }
        except Exception as e:
            return {
                'error': str(e),
                'status': 'error'
            }

if __name__ == "__main__":
    # 创建所有表
    tableinof = Image.get_database_status()
    print(tableinof)