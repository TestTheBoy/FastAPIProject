from typing import List

from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session


from database import get_session, transactional_session
from App_Demo.auth_middleware import SaCheckPermission, SaMode
from App_Demo.base import R, CommonPage, CommonResult, IdParam, IdsParam
from modules.sys.params.post_param import PostPageParam, PostParam
from modules.sys.services.post_service import PostService
# from modules.sys.vos.dict_vo import LabelValueVO
from modules.sys.vos.post_vo import PostVO

tags = ["岗位"]
router = APIRouter(tags=tags)


def get_post_service(db: Session = Depends(get_session)) -> PostService:
    """
    获取岗位服务实例的依赖函数
    """
    return PostService(db)


@router.post("/sys/post/save", summary="添加岗位", response_model=CommonResult, response_model_exclude_none=True)
@SaCheckPermission("sys:post:save")
async def post_save(data: PostParam = Body(description="岗位参数"), post_service: PostService = Depends(get_post_service)):
    with transactional_session(post_service.db):
        post_service.save(data)
    return R.success()


@router.post("/sys/post/update", summary="修改岗位", response_model=CommonResult, response_model_exclude_none=True)
@SaCheckPermission("sys:post:update")
async def post_update(data: PostParam = Body(description="岗位参数"), post_service: PostService = Depends(get_post_service)):
    with transactional_session(post_service.db):
        post_service.update(data)
    return R.success()


@router.post("/sys/post/remove", summary="删除岗位", response_model=CommonResult, response_model_exclude_none=True)
@SaCheckPermission("sys:post:remove")
async def post_remove(param: IdsParam = Body(), post_service: PostService = Depends(get_post_service)):
    with transactional_session(post_service.db):
        post_service.remove_by_ids(param.ids)
    return R.success()


@router.post("/sys/post/detail", summary="岗位详情", response_model=CommonResult[PostVO], response_model_exclude_none=True)
@SaCheckPermission(["sys:post:detail", "sys:post:update"], mode=SaMode.OR)
async def post_detail(param: IdParam = Body(), post_service: PostService = Depends(get_post_service)):
    data = post_service.detail(param.id)
    return R.data(data)


@router.post("/sys/post/page", summary="分页查询岗位列表", response_model=CommonResult[CommonPage[PostVO]], response_model_exclude_none=True)
@SaCheckPermission("sys:post:page")
async def post_page(param: PostPageParam = Body(), post_service: PostService = Depends(get_post_service)):
    data = post_service.page(param)
    return R.data(data)

# @router.post("/sys/post/select", summary="岗位下拉数据", response_model=CommonResult[List[LabelValueVO]], response_model_exclude_none=True)
# async def post_select(param: PostPageParam = Body(), post_service: PostService = Depends(get_post_service)):
#     posts:List[PostVO] = post_service.list(param)
#     res = [LabelValueVO(label=post.name, value=post.id) for post in posts]
#     return R.data(res)