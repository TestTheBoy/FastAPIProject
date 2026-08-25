from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session


from database import get_session, transactional_session
from App_Demo.auth_middleware import SaCheckPermission, SaMode
from App_Demo.base import R, CommonPage, CommonResult, IdParam, IdsParam
from modules.sys.params.config_param import ConfigPageParam, ConfigParam
from modules.sys.services.config_service import ConfigService
from modules.sys.vos.config_vo import ConfigVO

tags = ["配置"]
router = APIRouter(tags=tags)


def get_config_service(db: Session = Depends(get_session)) -> ConfigService:
    """
    获取配置服务实例的依赖函数
    """
    return ConfigService(db)


@router.post("/sys/config/save", summary="添加配置", response_model=CommonResult, response_model_exclude_none=True)
@SaCheckPermission("sys:config:save")
async def config_save(data: ConfigParam = Body(description="配置参数"), config_service: ConfigService = Depends(get_config_service)):
    with transactional_session(config_service.db):
        config_service.save(data)
    return R.success()


@router.post("/sys/config/update", summary="修改配置", response_model=CommonResult, response_model_exclude_none=True)
@SaCheckPermission("sys:config:update")
async def config_update(data: ConfigParam = Body(description="配置参数"), config_service: ConfigService = Depends(get_config_service)):
    with transactional_session(config_service.db):
        config_service.update(data)
    return R.success()


@router.post("/sys/config/remove", summary="删除配置", response_model=CommonResult, response_model_exclude_none=True)
@SaCheckPermission("sys:config:remove")
async def config_remove(param: IdsParam = Body(), config_service: ConfigService = Depends(get_config_service)):
    with transactional_session(config_service.db):
        config_service.remove_by_ids(param.ids)
    return R.success()


@router.post("/sys/config/detail", summary="配置详情", response_model=CommonResult[ConfigVO], response_model_exclude_none=True)
@SaCheckPermission(["sys:config:detail", "sys:config:update"], mode=SaMode.OR)
async def config_detail(param: IdParam = Body(), config_service: ConfigService = Depends(get_config_service)):
    data = config_service.detail(param.id)
    return R.data(data)


@router.post("/sys/config/page", summary="分页查询配置列表", response_model=CommonResult[CommonPage[ConfigVO]], response_model_exclude_none=True)
@SaCheckPermission("sys:config:page")
async def config_page(param: ConfigPageParam = Body(), config_service: ConfigService = Depends(get_config_service)):
    data = config_service.page(param)
    return R.data(data)
