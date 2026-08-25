from typing import List
from App_Demo.base import CommonPage
from App_Demo.low_code_util import LowCodeUtil
from App_Demo.util import OrmUtil
from modules.sys.models.role import RoleOrmModel
from modules.sys.params.role_param import RolePageParam, RoleParam
from modules.sys.vos.role_vo import RoleVO
from sqlalchemy.orm import Session, Query


class RoleService:
    def __init__(self, db: Session):
        self.model = RoleOrmModel
        self.db = db

    """
    角色服务
    """
    def save(self, param: RoleParam):
        """
        保存角色
        :param param: 角色参数
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

    def update(self, param: RoleParam):
        """
        修改角色（部分更新）
        :param param: 角色参数
        :return: bool
        """
        # 将参数对象转换为字典，只包含设置过的字段
        param_dict = param.model_dump(exclude_unset=True)
        # 移除 id 字段，避免更新 id
        param_dict.pop('id', None)
        # 过滤掉值为 None 的字段，避免将数据库中的字段更新为 NULL
        param_dict = {k: v for k, v in param_dict.items() if v is not None}
        # 直接更新数据库记录
        self.db.query(self.model).filter(self.model.id == param.id).update(param_dict)
        self.db.flush()
        return True

    def remove_by_ids(self, ids: List[str]):
        """
        删除角色（逻辑删除）
        :param ids: 角色id集合
        :return: bool
        """
        self.model.remove_by_ids(ids, self.db)
        self.db.flush()
        return True

    def detail(self, id: str) -> RoleVO:
        """
        角色详情
        :param id: 角色id
        :return: RoleVO
        """
        model = self.db.query(self.model).get(id)
        if not model:
            return None
        # 使用OrmUtil工具将model转换成vo
        return OrmUtil.to_vo(model, RoleVO)

    def list(self, param: RolePageParam) -> List[RoleVO]:
        """
        查询角色列表
        :param param: 查询参数
        :return: 角色列表
        """
        # 构建动态查询条件
        query: Query = LowCodeUtil.build_query(page_param=param, model=self.model,db=self.db, query=None)
        # 转换为vo-list
        return OrmUtil.to_list(query, RoleVO)

    def page(self, param: RolePageParam) -> CommonPage[RoleVO]:
        """
        分页查询角色
        :param param: 查询参数
        :return: 角色列表
        """
        pageNum = param.pageNum
        pageSize = param.pageSize
        # 构建动态查询条件
        query: Query = LowCodeUtil.build_query(page_param=param, model=self.model,db=self.db, query=None)
        # 转成通用分页对象
        return CommonPage.to_page(query, page_num=pageNum, page_size=pageSize, vo_class=RoleVO)