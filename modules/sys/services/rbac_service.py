from typing import List


from sqlalchemy.orm import Session, Query

from App_Demo.base import CommonPage
from App_Demo.user_context import UserContext
from App_Demo.util import OrmUtil
from modules.sys.models.role_menu import RoleMenuOrmModel
from modules.sys.models.user_role import UserRoleOrmModel
from modules.sys.params.menu_param import MenuPageParam
from modules.sys.params.role_menu_param import RoleMenuParam
from modules.sys.params.user_param import UserPageParam
from modules.sys.params.user_role_param import UserRoleParam
from modules.sys.services.menu_service import MenuService
from modules.sys.services.user_service import UserService
from modules.sys.vos.role_menu_vo import RoleMenuVO
from modules.sys.vos.user_role_vo import UserRoleVO
from modules.sys.vos.user_vo import UserVO


class RbacService:
    def __init__(self, db: Session):
        self.db = db

    def save_user_role(self, userRoleList: List[UserRoleParam]):
        """
        保存用户角色关联
        :param userRoleList: 用户角色关联集合
        :return:
        """
        if userRoleList:
            for userRole in userRoleList:
                count = self.db.query(UserRoleOrmModel).filter(UserRoleOrmModel.userId == userRole.userId,UserRoleOrmModel.roleId ==  userRole.roleId).count()
                if count > 0:
                    continue
                #创建模型实例
                model = UserRoleOrmModel(userId=userRole.userId,roleId=userRole.roleId)
                self.db.add(model)
        self.db.flush()
        return True

    def remove_user_role(self, userRoleList: List[UserRoleParam]):
        """
        根据用户ID删除用户角色关联
        :param userRoleList: 用户角色关联集合
        :return:
        """
        if userRoleList:
            for userRole in userRoleList:
                self.db.query(UserRoleOrmModel).filter(UserRoleOrmModel.userId == userRole.userId,
                                                       UserRoleOrmModel.roleId == userRole.roleId).delete()
        self.db.flush()
        return True

    def user_list_by_role_id(self,param: UserPageParam) -> CommonPage[UserVO]:
        """
        根据角色ID获取用户ID列表
        :param roleId: 角色ID
        :return:
        """
        userService = UserService(self.db)
        query: Query = self.db.query(UserRoleOrmModel).filter(UserRoleOrmModel.roleId == param.roleId)
        userRoleList: List[UserRoleVO] = OrmUtil.to_list(query, UserRoleVO)
        param.inUserIdList = [userRole.userId for userRole in userRoleList]
        if not param.inUserIdList:
            # 如果该角色没有用户，则返回空
            return CommonPage(recordCount=0, totalPage=0, pageNum=param.pageNum, pageSize=param.pageSize, rows=[])
        return userService.page(param)

    def user_list_exclude_role_id(self,param: UserPageParam) -> CommonPage[UserVO]:
        """
        获取用户ID列表-排除指定角色
        :param roleId: 角色ID
        :return:
        """
        userService = UserService(self.db)
        query: Query = self.db.query(UserRoleOrmModel).filter(UserRoleOrmModel.roleId == param.roleId)
        userRoleList: List[UserRoleVO] = OrmUtil.to_list(query, UserRoleVO)
        param.notInUserIdList = [userRole.userId for userRole in userRoleList]
        return userService.page(param)

    def save_role_menu(self, roleMenuList: List[RoleMenuParam]):
        '''
        保存角色菜单关联
        :param roleMenuList:角色菜单关联集合
        :return:
        '''
        if not roleMenuList: return True
        # 获取当前用户拥有的菜单ID列表
        menuService = MenuService(self.db)
        menu_ids = menuService.get_menu_ids_by_user_id(UserContext.get_current_user_id())
        is_super_admin = UserContext.is_super_admin()
        # 删除角色菜单关联
        self.db.query(RoleMenuOrmModel).filter(RoleMenuOrmModel.roleId == roleMenuList[0].roleId).delete()
        for roleMenu in roleMenuList:
            # 非超级管理员用户只能保存自己拥有菜单权限
            if not is_super_admin and str(roleMenu.menuId) not in menu_ids:
                continue
            # 创建模型实例
            model = RoleMenuOrmModel(roleId=roleMenu.roleId, menuId=roleMenu.menuId)
            self.db.add(model)
        self.db.flush()
        return True

    def role_menu_ids(self, roleId: str) -> List[str]:
        """
        根据角色ID获取菜单ID集合
        :param roleId: 角色ID
        :return:
        """
        query: Query = self.db.query(RoleMenuOrmModel).filter(RoleMenuOrmModel.roleId == roleId)
        roleMenuList: List[RoleMenuVO] = OrmUtil.to_list(query, RoleMenuVO)
        return [roleMenu.menuId for roleMenu in roleMenuList]

    def role_menu_tree(self, param: MenuPageParam) -> List[RoleMenuVO]:
        """
        获取角色菜单树
        :param param: 菜单参数
        :return: 菜单树
        """
        menuService = MenuService(self.db)
        param.filterByUser = 1
        return menuService.tree(param)