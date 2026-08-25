from typing import List
from App_Demo.base import CommonPage
from App_Demo.low_code_util import LowCodeUtil
from App_Demo.user_context import UserContext
from App_Demo.util import OrmUtil, TreeUtil
from modules.sys.models.menu import MenuOrmModel
from modules.sys.models.role_menu import RoleMenuOrmModel
from modules.sys.models.user_role import UserRoleOrmModel
from modules.sys.params.menu_param import MenuPageParam, MenuParam
from modules.sys.vos.menu_vo import MenuVO
from sqlalchemy.orm import Session, Query


class MenuService:
    def __init__(self, db: Session):
        self.model = MenuOrmModel
        self.db = db

    """
    菜单服务
    """
    def save(self, param: MenuParam):
        """
        保存菜单
        :param param: 菜单参数
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

    def update(self, param: MenuParam):
        """
        修改菜单（部分更新）
        :param param: 菜单参数
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
        删除菜单（逻辑删除）
        :param ids: 菜单id集合
        :return: bool
        """
        self.model.remove_by_ids(ids, self.db)
        self.db.flush()
        return True

    def detail(self, id: str) -> MenuVO:
        """
        菜单详情
        :param id: 菜单id
        :return: MenuVO
        """
        model = self.db.query(self.model).get(id)
        if not model:
            return None
        # 使用OrmUtil工具将model转换成vo
        return OrmUtil.to_vo(model, MenuVO)

    def list(self, param: MenuPageParam) -> List[MenuVO]:
        """
        查询菜单列表
        :param param: 查询参数
        :return: 菜单列表
        """
        # 构建动态查询条件
        query: Query = LowCodeUtil.build_query(page_param=param, model=self.model,db=self.db, query=None)
        # 转换为vo-list
        return OrmUtil.to_list(query, MenuVO)

    def page(self, param: MenuPageParam) -> CommonPage[MenuVO]:
        """
        分页查询菜单
        :param param: 查询参数
        :return: 菜单列表
        """
        pageNum = param.pageNum
        pageSize = param.pageSize
        # 构建动态查询条件
        query: Query = LowCodeUtil.build_query(page_param=param, model=self.model,db=self.db, query=None)
        # 转成通用分页对象
        return CommonPage.to_page(query, page_num=pageNum, page_size=pageSize, vo_class=MenuVO)

    def tree(self, param: MenuPageParam) -> List[MenuVO]:
        """
        获取菜单树
        :param param: 查询参数
        :return: 菜单树
        """
        listData:List[MenuVO] = self.list(param)
        if not UserContext.is_super_admin() and param.filterByUser == 1:
            #获取当前用户权限的菜单
            menu_ids = self.get_menu_ids_by_user_id(UserContext.get_current_user_id())
            #重新过滤数据，设置disabled
            for item in listData:
                if item.id not in menu_ids:
                    item.disabled = True
        # 转换为树结构
        return TreeUtil.build_tree(listData)

    def get_menu_ids_by_user_id(self,user_id:str) -> List[str]:
        '''
        通过用户ID获取菜单ID集合
        :param user_id: 用户ID
        :return: 菜单ID列表
        '''
        #获取用户的角色ID列表
        user_roles = self.db.query(UserRoleOrmModel).filter(UserRoleOrmModel.userId == user_id).all()
        role_ids = [user_role.roleId for user_role in user_roles]

        if not role_ids:
            return []

        #获取角色菜单关系
        role_menus = self.db.query(RoleMenuOrmModel).filter(RoleMenuOrmModel.roleId.in_(role_ids)).all()

        #获取菜单ID列表
        menu_ids = [str(role_menu.menuId) for role_menu in role_menus]
        return menu_ids