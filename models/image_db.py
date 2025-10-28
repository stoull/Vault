from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# 创建数据库引擎
database_url = "sqlite:///./images.db"
engine = create_engine(database_url, echo=True)

# 创建Session
Session = sessionmaker(bind=engine)
session = Session()

# 创建基础模型类
Base = declarative_base()

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid_filename = Column(String(100), unique=True, nullable=False, index=True)
    original_filename = Column(String(255), nullable=False)
    file_size = Column(Integer)
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
            'filename': self.uuid_filename,
            'original_name': self.original_filename,
            'url': f"/images/{self.uuid_filename}",
            'thumbnail_url': f"/images/thumbnails/{self.uuid_filename}",
            'size': self.file_size,
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