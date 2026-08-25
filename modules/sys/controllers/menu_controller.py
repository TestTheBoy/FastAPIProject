from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

from typing import List

from database import get_session, transactional_session
from App_Demo.auth_middleware import SaCheckPermission, SaMode
from App_Demo.base import R, CommonResult, IdParam, IdsParam

from modules.sys.params.menu_param import MenuPageParam, MenuParam
from modules.sys.services.menu_service import MenuService
from modules.sys.vos.menu_vo import MenuVO

tags = ["菜单"]
router = APIRouter(tags=tags)


def get_menu_service(db: Session = Depends(get_session)) -> MenuService:
    """
    获取菜单服务实例的依赖函数
    """
    return MenuService(db)


@router.post("/sys/menu/save", summary="添加菜单", response_model=CommonResult, response_model_exclude_none=True)
@SaCheckPermission("sys:menu:save")
async def menu_save(data: MenuParam = Body(description="菜单参数"), menu_service: MenuService = Depends(get_menu_service)):
    with transactional_session(menu_service.db):
        menu_service.save(data)
    return R.success()


@router.post("/sys/menu/update", summary="修改菜单", response_model=CommonResult, response_model_exclude_none=True)
@SaCheckPermission("sys:menu:update")
async def menu_update(data: MenuParam = Body(description="菜单参数"), menu_service: MenuService = Depends(get_menu_service)):
    with transactional_session(menu_service.db):
        menu_service.update(data)
    return R.success()


@router.post("/sys/menu/remove", summary="删除菜单", response_model=CommonResult, response_model_exclude_none=True)
@SaCheckPermission("sys:menu:remove")
async def menu_remove(param: IdsParam = Body(), menu_service: MenuService = Depends(get_menu_service)):
    with transactional_session(menu_service.db):
        menu_service.remove_by_ids(param.ids)
    return R.success()


@router.post("/sys/menu/detail", summary="菜单详情", response_model=CommonResult[MenuVO], response_model_exclude_none=True)
@SaCheckPermission(["sys:menu:detail", "sys:menu:update"], mode=SaMode.OR)
async def menu_detail(param: IdParam = Body(), menu_service: MenuService = Depends(get_menu_service)):
    data = menu_service.detail(param.id)
    return R.data(data)


@router.post("/sys/menu/list", summary="菜单列表", response_model=CommonResult[List[MenuVO]], response_model_exclude_none=True)
@SaCheckPermission("sys:menu:list")
async def menu_list(param: MenuPageParam = Body(), menu_service: MenuService = Depends(get_menu_service)):
    data = menu_service.list(param)
    return R.data(data)

@router.post("/sys/menu/tree", summary="菜单树", response_model=CommonResult[List[MenuVO]], response_model_exclude_none=True)
@SaCheckPermission("sys:menu:tree")
async def menu_tree(param: MenuPageParam = Body(), menu_service: MenuService = Depends(get_menu_service)):
    data = menu_service.tree(param)
    return R.data(data)
