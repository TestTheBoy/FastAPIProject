
import logging
from typing import  List
from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

from App_Demo.low_code_util import LowCodeUtil
from App_Demo.util import StrUtil
from database import get_session

from App_Demo.base import R, BasePageParam, CommonResult
from modules.sys.vos.dict_vo import LabelValueVO

tags = ["低代码接口"]

router = APIRouter(tags=tags)

@router.post("/{moduleName}/{tableName}/select", summary="通用下拉", tags=tags, response_model=CommonResult[List[LabelValueVO]], response_model_exclude_none=True)
async def select(
    moduleName: str, 
    tableName: str, 
    param: BasePageParam = Body(description="查询参数"), 
    db: Session = Depends(get_session)
):
    return R.data(LowCodeUtil.select(moduleName, tableName, param, db,True))

# @router.post("/badgeConfig",summary="获取徽标配置",tags=tags,response_model=CommonResult[List[MenuBadgeConfig]],response_model_exclude_none=True)
# async def badge_config():

#     return R.data(badge_configs)