from fastapi import APIRouter, Depends,Body
from typing import List
from sqlalchemy.orm import Session

from App_Demo.auth_middleware import SaCheckPermission
from App_Demo.base import CommonResult,R,CommonPage
from database import get_session, transactional_session
from modules.sys.params.menu_param import MenuParam
from modules.sys.params.user_role_param import UserRoleParam
from modules.sys.services.rbac_service import RbacService
from App_Demo.auth_middleware import SaCheckPermission,SaMode
from modules.sys.vos.menu_vo import MenuVO
from modules.sys.vos.user_vo import UserVO
from modules.sys.params.user_param import UserPageParam
from modules.sys.params.role_menu_param import RoleMenuParam,RoleIdParam
from modules.sys.params.menu_param import MenuPageParam

tags = ["RBAC相关接口"]
router = APIRouter(tags=tags)


def get_rbac_service(db: Session = Depends(get_session)) -> RbacService:
    """
    获取rbac服务示例的依赖函数
    :param db:
    :return:
    """
    return RbacService(db)

@router.post("/sys/rbac/saveUserRole", summary="添加用户角色", response_model=CommonResult, response_model_exclude_none=True)
@SaCheckPermission("sys:rbac:saveUserRole")
async def save_user_role(data: List[UserRoleParam] = Body(description="用户角色参数"), rbac_service: RbacService = Depends(get_rbac_service)):
    with transactional_session(rbac_service.db):
        rbac_service.save_user_role(data)
    return R.success()


@router.post("/sys/rbac/removeUserRole", summary="删除用户角色", response_model=CommonResult, response_model_exclude_none=True)
@SaCheckPermission("sys:rbac:removeUserRole")
async def remove_user_role(data: List[UserRoleParam] = Body(description="用户角色参数"), rbac_service: RbacService = Depends(get_rbac_service)):
    with transactional_session(rbac_service.db):
        rbac_service.remove_user_role(data)
    return R.success()


@router.post("/sys/rbac/userListByRoleId", summary="通过角色ID获取用户列表", response_model=CommonResult[CommonPage[UserVO]], response_model_exclude_none=True)
@SaCheckPermission("sys:rbac:userListByRoleId")
async def user_list_by_role_id(param: UserPageParam = Body(), rbac_service: RbacService = Depends(get_rbac_service)):
    data = rbac_service.user_list_by_role_id(param)
    return R.data(data)

@router.post("/sys/rbac/userListExcludeRoleId", summary="获取用户列表-排除指定角色", response_model=CommonResult[CommonPage[UserVO]], response_model_exclude_none=True)
@SaCheckPermission(value=["sys:rbac:userListExcludeRoleId","sys:rbac:saveUserRole"], mode=SaMode.OR)
async def user_list_exclude_role_id(param: UserPageParam = Body(), rbac_service: RbacService = Depends(get_rbac_service)):
    data = rbac_service.user_list_exclude_role_id(param)
    return R.data(data)

@router.post("/sys/rbac/saveRoleMenu", summary="保存角色菜单", response_model=CommonResult, response_model_exclude_none=True)
@SaCheckPermission("sys:rbac:saveRoleMenu")
async def save_role_menu(data: List[RoleMenuParam] = Body(description="角色菜单参数"), rbac_service: RbacService = Depends(get_rbac_service)):
    with transactional_session(rbac_service.db):
        rbac_service.save_role_menu(data)
    return R.success()


@router.post("/sys/rbac/roleMenuIds", summary="根据角色ID获取菜单ID集合", response_model=CommonResult[List[str]], response_model_exclude_none=True)
@SaCheckPermission(value=["sys:rbac:roleMenuIds","sys:rbac:saveRoleMenu"], mode=SaMode.OR)
async def role_menu_ids(param: RoleIdParam = Body(), rbac_service: RbacService = Depends(get_rbac_service)):
    data = rbac_service.role_menu_ids(param.roleId)
    return R.data(data)

@router.post("/sys/rbac/roleMenuTree", summary="获取权限菜单树", response_model=CommonResult[List[MenuVO]], response_model_exclude_none=True)
@SaCheckPermission(value=["sys:rbac:roleMenuTree","sys:rbac:saveRoleMenu"], mode=SaMode.OR)
async def role_menu_tree(param: MenuPageParam = Body(), rbac_service: RbacService = Depends(get_rbac_service)):
    data = rbac_service.role_menu_tree(param)
    return R.data(data)