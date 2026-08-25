from pydantic import BaseModel, Field
from typing import Optional


from App_Demo.base import BasePageParam


class FileInfoParam(BaseModel):
    id: Optional[str] = Field(None, title="主键", description="主键")

    
    
    url: str = Field(..., title="文件访问地址", description="文件访问地址")
    
    size: Optional[str] = Field(None, title="文件大小，单位字节", description="文件大小，单位字节")
    
    sizeInfo: Optional[str] = Field(None, title="文件大小，有单位", description="文件大小，有单位")
    
    filename: Optional[str] = Field(None, title="文件名称", description="文件名称")
    
    originalFilename: Optional[str] = Field(None, title="原始文件名", description="原始文件名")
    
    basePath: Optional[str] = Field(None, title="基础存储路径", description="基础存储路径")
    
    path: Optional[str] = Field(None, title="存储路径", description="存储路径")
    
    ext: Optional[str] = Field(None, title="文件扩展名", description="文件扩展名")
    
    contentType: Optional[str] = Field(None, title="MIME类型", description="MIME类型")
    
    platform: Optional[str] = Field(None, title="存储平台", description="存储平台")
    
    thUrl: Optional[str] = Field(None, title="缩略图访问路径", description="缩略图访问路径")
    
    thFilename: Optional[str] = Field(None, title="缩略图大小，单位字节", description="缩略图大小，单位字节")
    
    thSize: Optional[str] = Field(None, title="缩略图大小，单位字节", description="缩略图大小，单位字节")
    
    thSizeInfo: Optional[str] = Field(None, title="缩略图大小，有单位", description="缩略图大小，有单位")
    
    thContentType: Optional[str] = Field(None, title="缩略图MIME类型", description="缩略图MIME类型")
    
    objectId: Optional[str] = Field(None, title="文件所属对象id", description="文件所属对象id")
    
    objectType: Optional[str] = Field(None, title="文件所属对象类型，例如用户头像，评价图片", description="文件所属对象类型，例如用户头像，评价图片")
    
    attr: Optional[str] = Field(None, title="附加属性", description="附加属性")
    
    
    
    
    


class FileInfoPageParam(BasePageParam):
    pass