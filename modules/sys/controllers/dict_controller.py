from typing import List

from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session


from database import get_session, transactional_session
from App_Demo.auth_middleware import SaCheckPermission, SaMode
from App_Demo.base import R, CommonPage, CommonResult, IdParam, IdsParam
from modules.sys.params.dict_param import DictPageParam, DictParam, DictTypeParam
from modules.sys.services.dict_service import DictService
from modules.sys.vos.dict_vo import DictVO, LabelValueVO

tags = ["字典"]
router = APIRouter(tags=tags)


def get_dict_service(db: Session = Depends(get_session)) -> DictService:
    """
    获取字典服务实例的依赖函数
    """
    return DictService(db)


@router.post("/sys/dict/save", summary="添加字典", response_model=CommonResult, response_model_exclude_none=True)
@SaCheckPermission("sys:dict:save")
async def dict_save(data: DictParam = Body(description="字典参数"), dict_service: DictService = Depends(get_dict_service)):
    with transactional_session(dict_service.db):
        dict_service.save(data)
    return R.success()


@router.post("/sys/dict/update", summary="修改字典", response_model=CommonResult, response_model_exclude_none=True)
@SaCheckPermission("sys:dict:update")
async def dict_update(data: DictParam = Body(description="字典参数"), dict_service: DictService = Depends(get_dict_service)):
    with transactional_session(dict_service.db):
        dict_service.update(data)
    return R.success()


@router.post("/sys/dict/remove", summary="删除字典", response_model=CommonResult, response_model_exclude_none=True)
@SaCheckPermission("sys:dict:remove")
async def dict_remove(param: IdsParam = Body(), dict_service: DictService = Depends(get_dict_service)):
    with transactional_session(dict_service.db):
        dict_service.remove_by_ids(param.ids)
    return R.success()


@router.post("/sys/dict/detail", summary="字典详情", response_model=CommonResult[DictVO], response_model_exclude_none=True)
@SaCheckPermission(["sys:dict:detail", "sys:dict:update"], mode=SaMode.OR)
async def dict_detail(param: IdParam = Body(), dict_service: DictService = Depends(get_dict_service)):
    data = dict_service.detail(param.id)
    return R.data(data)


@router.post("/sys/dict/page", summary="分页查询字典列表", response_model=CommonResult[CommonPage[DictVO]], response_model_exclude_none=True)
@SaCheckPermission("sys:dict:page")
async def dict_page(param: DictPageParam = Body(), dict_service: DictService = Depends(get_dict_service)):
    data = dict_service.page(param)
    return R.data(data)

@router.post("/sys/dict/getByDictType", summary="根据字典编码获取字典", response_model=CommonResult[List[LabelValueVO]], response_model_exclude_none=True)
async def get_by_dict_type(param: DictTypeParam = Body(), dict_service: DictService = Depends(get_dict_service)):
    data = dict_service.get_by_dict_type(param.dictType)
    return R.data(data)