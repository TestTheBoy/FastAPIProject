#服务层/角色管理控制器封装
from typing import List

from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session, Query

from App_Demo.auth_middleware import SaCheckPermission, SaMode
from App_Demo.base import R, CommonResult, IdParam, IdsParam, BasePageParam, CommonPage, APIModel
from App_Demo.util import OrmUtil
from database import get_session, transactional_session
from modules.sys.services.role_service import RoleService
from modules.sys.models.role import RoleOrmModel
from modules.sys.params.role_param import RoleParam, RolePageParam
# from modules.sys.vos.dict_vo import LabelValueVO
from modules.sys.vos.dict_vo import LabelValueVO
from modules.sys.vos.role_vo import RoleVO

router = APIRouter(tags=["角色管理"],prefix="")

def get_role_service(db: Session = Depends(get_session)):
    """
    获取角色服务实例的依赖函数
    """
    return RoleService(db)

@router.post("/sys/role/save", summary="添加角色", response_model=CommonResult, response_model_exclude_none=True)
@SaCheckPermission("sys:role:save")
async def role_save(data: RoleParam = Body(description="角色参数"), role_service: RoleService = Depends(get_role_service)):
    with transactional_session(role_service.db):
        role_service.save(data)
    return R.success()


@router.post("/sys/role/update", summary="修改角色", response_model=CommonResult, response_model_exclude_none=True)
@SaCheckPermission("sys:role:update")
async def role_update(data: RoleParam = Body(description="角色参数"), role_service: RoleService = Depends(get_role_service)):
    with transactional_session(role_service.db):
        role_service.update(data)
    return R.success()


@router.post("/sys/role/remove", summary="删除角色", response_model=CommonResult, response_model_exclude_none=True)
@SaCheckPermission("sys:role:remove")
async def role_remove(param: IdsParam = Body(), role_service: RoleService = Depends(get_role_service)):
    with transactional_session(role_service.db):
        role_service.remove_by_ids(param.ids)
    return R.success()


@router.post("/sys/role/detail", summary="角色详情", response_model=CommonResult[RoleVO], response_model_exclude_none=True)
@SaCheckPermission(["sys:role:detail", "sys:role:update"], mode=SaMode.OR)
async def role_detail(param: IdParam = Body(), role_service: RoleService = Depends(get_role_service)):
    data = role_service.detail(param.id)
    return R.data(data)


@router.post("/sys/role/page", summary="分页查询角色列表", response_model=CommonResult[CommonPage[RoleVO]], response_model_exclude_none=True)
@SaCheckPermission("sys:role:page")
async def role_page(param: RolePageParam = Body(), role_service: RoleService = Depends(get_role_service)):
    data = role_service.page(param)
    return R.data(data)


@router.post("/sys/role/select", summary="角色下拉数据", response_model=CommonResult[List[LabelValueVO]], response_model_exclude_none=True)
async def role_select(param: RolePageParam = Body(), role_service: RoleService = Depends(get_role_service)):
    roles:List[RoleVO] = role_service.list(param)
    res = [LabelValueVO(label=role.name, value=role.id) for role in roles]
    return R.data(res)
