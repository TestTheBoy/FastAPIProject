from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

from typing import List

from database import get_session, transactional_session
from App_Demo.auth_middleware import SaCheckPermission, SaMode
from App_Demo.base import R, CommonResult, IdParam, IdsParam

from modules.sys.params.dept_param import DeptPageParam, DeptParam
from modules.sys.services.dept_service import DeptService
from modules.sys.vos.dept_vo import DeptVO

tags = ["部门"]
router = APIRouter(tags=tags)


def get_dept_service(db: Session = Depends(get_session)) -> DeptService:
    """
    获取部门服务实例的依赖函数
    """
    return DeptService(db)


@router.post("/sys/dept/save", summary="添加部门", response_model=CommonResult, response_model_exclude_none=True)
@SaCheckPermission("sys:dept:save")
async def dept_save(data: DeptParam = Body(description="部门参数"), dept_service: DeptService = Depends(get_dept_service)):
    with transactional_session(dept_service.db):
        dept_service.save(data)
    return R.success()


@router.post("/sys/dept/update", summary="修改部门", response_model=CommonResult, response_model_exclude_none=True)
@SaCheckPermission("sys:dept:update")
async def dept_update(data: DeptParam = Body(description="部门参数"), dept_service: DeptService = Depends(get_dept_service)):
    with transactional_session(dept_service.db):
        dept_service.update(data)
    return R.success()


@router.post("/sys/dept/remove", summary="删除部门", response_model=CommonResult, response_model_exclude_none=True)
@SaCheckPermission("sys:dept:remove")
async def dept_remove(param: IdsParam = Body(), dept_service: DeptService = Depends(get_dept_service)):
    with transactional_session(dept_service.db):
        dept_service.remove_by_ids(param.ids)
    return R.success()


@router.post("/sys/dept/detail", summary="部门详情", response_model=CommonResult[DeptVO], response_model_exclude_none=True)
@SaCheckPermission(["sys:dept:detail", "sys:dept:update"], mode=SaMode.OR)
async def dept_detail(param: IdParam = Body(), dept_service: DeptService = Depends(get_dept_service)):
    data = dept_service.detail(param.id)
    return R.data(data)


@router.post("/sys/dept/list", summary="部门列表", response_model=CommonResult[List[DeptVO]], response_model_exclude_none=True)
@SaCheckPermission("sys:dept:list")
async def dept_list(param: DeptPageParam = Body(), dept_service: DeptService = Depends(get_dept_service)):
    data = dept_service.list(param)
    return R.data(data)

@router.post("/sys/dept/tree", summary="部门树", response_model=CommonResult[List[DeptVO]], response_model_exclude_none=True)
@SaCheckPermission(value=["sys:dept:tree","sys:user:page"],mode=SaMode.OR)
async def dept_tree(param: DeptPageParam = Body(), dept_service: DeptService = Depends(get_dept_service)):
    data = dept_service.tree(param)
    return R.data(data)
