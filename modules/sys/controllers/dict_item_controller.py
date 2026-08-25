from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session


from database import get_session, transactional_session
from App_Demo.auth_middleware import SaCheckPermission, SaMode
from App_Demo.base import R, CommonPage, CommonResult, IdParam, IdsParam
from modules.sys.params.dict_item_param import DictItemPageParam, DictItemParam
from modules.sys.services.dict_item_service import DictItemService
from modules.sys.vos.dict_item_vo import DictItemVO

tags = ["字典项"]
router = APIRouter(tags=tags)


def get_dict_item_service(db: Session = Depends(get_session)) -> DictItemService:
    """
    获取字典项服务实例的依赖函数
    """
    return DictItemService(db)


@router.post("/sys/dictItem/save", summary="添加字典项", response_model=CommonResult, response_model_exclude_none=True)
@SaCheckPermission("sys:dictItem:save")
async def dict_item_save(data: DictItemParam = Body(description="字典项参数"), dict_item_service: DictItemService = Depends(get_dict_item_service)):
    with transactional_session(dict_item_service.db):
        dict_item_service.save(data)
    return R.success()


@router.post("/sys/dictItem/update", summary="修改字典项", response_model=CommonResult, response_model_exclude_none=True)
@SaCheckPermission("sys:dictItem:update")
async def dict_item_update(data: DictItemParam = Body(description="字典项参数"), dict_item_service: DictItemService = Depends(get_dict_item_service)):
    with transactional_session(dict_item_service.db):
        dict_item_service.update(data)
    return R.success()


@router.post("/sys/dictItem/remove", summary="删除字典项", response_model=CommonResult, response_model_exclude_none=True)
@SaCheckPermission("sys:dictItem:remove")
async def dict_item_remove(param: IdsParam = Body(), dict_item_service: DictItemService = Depends(get_dict_item_service)):
    with transactional_session(dict_item_service.db):
        dict_item_service.remove_by_ids(param.ids)
    return R.success()


@router.post("/sys/dictItem/detail", summary="字典项详情", response_model=CommonResult[DictItemVO], response_model_exclude_none=True)
@SaCheckPermission(["sys:dictItem:detail", "sys:dictItem:update"], mode=SaMode.OR)
async def dict_item_detail(param: IdParam = Body(), dict_item_service: DictItemService = Depends(get_dict_item_service)):
    data = dict_item_service.detail(param.id)
    return R.data(data)


@router.post("/sys/dictItem/page", summary="分页查询字典项列表", response_model=CommonResult[CommonPage[DictItemVO]], response_model_exclude_none=True)
@SaCheckPermission("sys:dictItem:page")
async def dict_item_page(param: DictItemPageParam = Body(), dict_item_service: DictItemService = Depends(get_dict_item_service)):
    data = dict_item_service.page(param)
    return R.data(data)
