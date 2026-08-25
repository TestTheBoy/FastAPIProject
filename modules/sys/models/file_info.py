
from App_Demo.db_types import db_types
from pydantic import Field
from App_Demo.base import APIModel
from App_Demo.base import BaseOrmModel

from typing import Optional


# 数据库模型
class FileInfoOrmModel(BaseOrmModel):
    """
    文件信息数据库模型
    """
    __tablename__ = 'sys_file_info'
    
    # 如果数据库中不存在基类字段，则设置为None（不映射到数据库列）
    isDeleted = None
    
    # SQLAlchemy字段定义
    url: str = db_types.Column(db_types.String(64), name="url", nullable=False, comment="文件访问地址")
    size: str = db_types.Column(db_types.BigInteger, name="size", nullable=True, comment="文件大小，单位字节")
    sizeInfo: str = db_types.Column(db_types.String(64), name="size_info", nullable=True, comment="文件大小，有单位")
    filename: str = db_types.Column(db_types.String(255), name="filename", nullable=True, comment="文件名称")
    originalFilename: str = db_types.Column(db_types.String(255), name="original_filename", nullable=True, comment="原始文件名")
    basePath: str = db_types.Column(db_types.String(64), name="base_path", nullable=True, comment="基础存储路径")
    path: str = db_types.Column(db_types.String(64), name="path", nullable=True, comment="存储路径")
    ext: str = db_types.Column(db_types.String(32), name="ext", nullable=True, comment="文件扩展名")
    contentType: str = db_types.Column(db_types.String(100), name="content_type", nullable=True, comment="MIME类型")
    platform: str = db_types.Column(db_types.String(32), name="platform", nullable=True, comment="存储平台")
    thUrl: str = db_types.Column(db_types.String(255), name="th_url", nullable=True, comment="缩略图访问路径")
    thFilename: str = db_types.Column(db_types.String(255), name="th_filename", nullable=True, comment="缩略图大小，单位字节")
    thSize: str = db_types.Column(db_types.BigInteger, name="th_size", nullable=True, comment="缩略图大小，单位字节")
    thSizeInfo: str = db_types.Column(db_types.String(64), name="th_size_info", nullable=True, comment="缩略图大小，有单位")
    thContentType: str = db_types.Column(db_types.String(32), name="th_content_type", nullable=True, comment="缩略图MIME类型")
    objectId: str = db_types.Column(db_types.String(32), name="object_id", nullable=True, comment="文件所属对象id")
    objectType: str = db_types.Column(db_types.String(32), name="object_type", nullable=True, comment="文件所属对象类型，例如用户头像，评价图片")
    attr: str = db_types.Column(db_types.String(None), name="attr", nullable=True, comment="附加属性")

# Pydantic模型
class FileInfo(APIModel):
    """
    文件信息Pydantic模型，用于API接口
    """
    # Pydantic字段定义
    url: str = Field(None, description="文件访问地址")
    size: Optional[str] = Field(None, description="文件大小，单位字节")
    sizeInfo: Optional[str] = Field(None, description="文件大小，有单位")
    filename: Optional[str] = Field(None, description="文件名称")
    originalFilename: Optional[str] = Field(None, description="原始文件名")
    basePath: Optional[str] = Field(None, description="基础存储路径")
    path: Optional[str] = Field(None, description="存储路径")
    ext: Optional[str] = Field(None, description="文件扩展名")
    contentType: Optional[str] = Field(None, description="MIME类型")
    platform: Optional[str] = Field(None, description="存储平台")
    thUrl: Optional[str] = Field(None, description="缩略图访问路径")
    thFilename: Optional[str] = Field(None, description="缩略图大小，单位字节")
    thSize: Optional[str] = Field(None, description="缩略图大小，单位字节")
    thSizeInfo: Optional[str] = Field(None, description="缩略图大小，有单位")
    thContentType: Optional[str] = Field(None, description="缩略图MIME类型")
    objectId: Optional[str] = Field(None, description="文件所属对象id")
    objectType: Optional[str] = Field(None, description="文件所属对象类型，例如用户头像，评价图片")
    attr: Optional[str] = Field(None, description="附加属性")