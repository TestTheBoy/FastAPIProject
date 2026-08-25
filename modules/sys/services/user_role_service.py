from typing import List
from App_Demo.base import CommonPage
from App_Demo.util import OrmUtil
from modules.sys.models.user_role import UserRoleOrmModel
from modules.sys.params.user_role_param import UserRolePageParam, UserRoleParam
from modules.sys.vos.user_role_vo import UserRoleVO
from sqlalchemy.orm import Session, Query


class UserRoleService:
    def __init__(self, db: Session):
        self.model = UserRoleOrmModel
        self.db = db

    """
    r_用户角色关系服务
    """
    def save(self, param: UserRoleParam):
        """
        保存r_用户角色关系
        :param param: r_用户角色关系参数
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

    def update(self, param: UserRoleParam):
        """
        修改r_用户角色关系（部分更新）
        :param param: r_用户角色关系参数
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
        删除r_用户角色关系（逻辑删除）
        :param ids: r_用户角色关系id集合
        :return: bool
        """
        self.model.remove_by_ids(ids, self.db)
        self.db.flush()
        return True

    def detail(self, id: str) -> UserRoleVO:
        """
        r_用户角色关系详情
        :param id: r_用户角色关系id
        :return: UserRoleVO
        """
        model = self.db.query(self.model).get(id)
        if not model:
            return None
        # 使用OrmUtil工具将model转换成vo
        return OrmUtil.to_vo(model, UserRoleVO)

    def list(self, param: UserRolePageParam) -> List[UserRoleVO]:
        """
        查询r_用户角色关系列表
        :param param: 查询参数
        :return: r_用户角色关系列表
        """
        # 构建动态查询条件
        query: Query = self.db.query(self.model)
        # 转换为vo-list
        return OrmUtil.to_list(query, UserRoleVO)

    def page(self, param: UserRolePageParam) -> CommonPage[UserRoleVO]:
        """
        分页查询r_用户角色关系
        :param param: 查询参数
        :return: r_用户角色关系列表
        """
        pageNum = param.pageNum
        pageSize = param.pageSize
        # 构建动态查询条件
        query: Query = self.db.query(self.model)
        # 转成通用分页对象
        return CommonPage.to_page(query, page_num=pageNum, page_size=pageSize, vo_class=UserRoleVO)