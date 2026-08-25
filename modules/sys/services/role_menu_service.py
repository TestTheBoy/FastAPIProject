from typing import List
from App_Demo.base import CommonPage
from App_Demo.util import OrmUtil
from modules.sys.models.role_menu import RoleMenuOrmModel
from modules.sys.params.role_menu_param import RoleMenuPageParam, RoleMenuParam
from modules.sys.vos.role_menu_vo import RoleMenuVO
from sqlalchemy.orm import Session, Query


class RoleMenuService:
    def __init__(self, db: Session):
        self.model = RoleMenuOrmModel
        self.db = db

    """
    r_角色菜单关系服务
    """
    def save(self, param: RoleMenuParam):
        """
        保存r_角色菜单关系
        :param param: r_角色菜单关系参数
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

    def update(self, param: RoleMenuParam):
        """
        修改r_角色菜单关系（部分更新）
        :param param: r_角色菜单关系参数
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
        删除r_角色菜单关系（逻辑删除）
        :param ids: r_角色菜单关系id集合
        :return: bool
        """
        self.model.remove_by_ids(ids, self.db)
        self.db.flush()
        return True

    def detail(self, id: str) -> RoleMenuVO:
        """
        r_角色菜单关系详情
        :param id: r_角色菜单关系id
        :return: RoleMenuVO
        """
        model = self.db.query(self.model).get(id)
        if not model:
            return None
        # 使用OrmUtil工具将model转换成vo
        return OrmUtil.to_vo(model, RoleMenuVO)

    def list(self, param: RoleMenuPageParam) -> List[RoleMenuVO]:
        """
        查询r_角色菜单关系列表
        :param param: 查询参数
        :return: r_角色菜单关系列表
        """
        # 构建动态查询条件
        query: Query = self.db.query(self.model)
        # 转换为vo-list
        return OrmUtil.to_list(query, RoleMenuVO)

    def page(self, param: RoleMenuPageParam) -> CommonPage[RoleMenuVO]:
        """
        分页查询r_角色菜单关系
        :param param: 查询参数
        :return: r_角色菜单关系列表
        """
        pageNum = param.pageNum
        pageSize = param.pageSize
        # 构建动态查询条件
        query: Query = self.db.query(self.model)
        # 转成通用分页对象
        return CommonPage.to_page(query, page_num=pageNum, page_size=pageSize, vo_class=RoleMenuVO)