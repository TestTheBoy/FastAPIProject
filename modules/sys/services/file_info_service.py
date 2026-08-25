from typing import List

from fastapi import HTTPException, UploadFile
from App_Demo.base import CommonPage
from App_Demo.file_validator import FileValidator
from App_Demo.low_code_util import LowCodeUtil
from App_Demo.util import OrmUtil
from modules.sys.models.file_info import FileInfoOrmModel
from modules.sys.params.file_info_param import FileInfoPageParam, FileInfoParam
from modules.sys.vos.file_info_vo import FileInfoVO
from sqlalchemy.orm import Session, Query


class FileInfoService:
    def __init__(self, db: Session):
        self.model = FileInfoOrmModel
        self.db = db

    """
    文件信息服务
    """
    def save(self, param: FileInfoParam):
        """
        保存文件信息
        :param param: 文件信息参数
        :return: bool
        """
        # 将参数对象转换为字典
        param_dict = param.model_dump(exclude_unset=True)
        # 移除id字段，确保使用系统生成的ID
        param_dict.pop('id', None)
        # 创建模型实例
        model = self.model(**param_dict)
        self.db.add(model)
        self.db.flush()
        return True

    def update(self, param: FileInfoParam):
        """
        修改文件信息（部分更新）
        :param param: 文件信息参数
        :return: bool
        """
        # 将参数对象转换为字典，只包含设置过的字段
        param_dict = param.model_dump(exclude_unset=True)
        # 移除id字段，避免更新id
        param_dict.pop('id', None)
        # 直接更新数据库记录
        self.db.query(self.model).filter(self.model.id == param.id).update(param_dict)
        self.db.flush()
        return True

    def remove_by_ids(self, ids: List[str]):
        """
        删除文件信息（逻辑删除）
        :param ids: 文件信息id集合
        :return: bool
        """
        self.model.remove_by_ids(ids, self.db)
        self.db.flush()
        return True

    def detail(self, id: str) -> FileInfoVO:
        """
        文件信息详情
        :param id: 文件信息id
        :return: FileInfoVO
        """
        model = self.db.query(self.model).get(id)
        if not model:
            return None
        # 使用OrmUtil工具将model转换成vo
        return OrmUtil.to_vo(model, FileInfoVO)

    def list(self, param: FileInfoPageParam) -> List[FileInfoVO]:
        """
        查询文件信息列表
        :param param: 查询参数
        :return: 文件信息列表
        """
        # 构建动态查询条件
        query: Query = LowCodeUtil.build_query(page_param=param, model=self.model,db=self.db, query=None)
        # 转换为vo-list
        return OrmUtil.to_list(query, FileInfoVO)

    def page(self, param: FileInfoPageParam) -> CommonPage[FileInfoVO]:
        """
        分页查询文件信息
        :param param: 查询参数
        :return: 文件信息列表
        """
        pageNum = param.pageNum
        pageSize = param.pageSize
        # 构建动态查询条件
        query: Query = LowCodeUtil.build_query(page_param=param, model=self.model,db=self.db, query=None)
        # 转成通用分页对象
        return CommonPage.to_page(query, page_num=pageNum, page_size=pageSize, vo_class=FileInfoVO)
    
    @staticmethod
    def validate_avatar(file: UploadFile):
        # 1. 调用框架层的通用校验，限制头像最大2MB
        img, contents = FileValidator.validate_image(file, max_size_mb=2)
        
        # 2. 头像业务规则：最小 50x50（不再强制正方形，后续可加上）
        width, height = img.size
        if width < 50 or height < 50:
            raise HTTPException(400, "头像图片尺寸不能小于 50x50 像素")
        
        # 校验通过，重置指针，返回
        file.file.seek(0)
        return file