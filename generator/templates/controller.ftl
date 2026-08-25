from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session
{# 这里使用了Jinja2 模板语法 #}
{% if table.treeTable %}from typing import List{% endif %}

from database import get_session, transactional_session
from App_Demo.auth_middleware import SaCheckPermission, SaMode
from App_Demo.base import R, {% if not table.treeTable %}CommonPage, {% endif %}CommonResult, IdParam, IdsParam

from modules.{{ table.moduleName }}.params.{{ table.shortTableName }}_param import {{ table.tableHumpName }}PageParam, {{ table.tableHumpName }}Param
from modules.{{ table.moduleName }}.services.{{ table.shortTableName }}_service import {{ table.tableHumpName }}Service
from modules.{{ table.moduleName }}.vos.{{ table.shortTableName }}_vo import {{ table.tableHumpName }}VO

tags = ["{{ table.comment }}"]
router = APIRouter(tags=tags)


def get_{{ table.shortTableName }}_service(db: Session = Depends(get_session)) -> {{ table.tableHumpName }}Service:
    """
    获取{{ table.comment }}服务实例的依赖函数
    """
    return {{ table.tableHumpName }}Service(db)


@router.post("/{{ table.moduleName }}/{{ table.tableCamelName }}/save", summary="添加{{ table.comment }}", response_model=CommonResult, response_model_exclude_none=True)
@SaCheckPermission("{{ table.moduleName }}:{{ table.tableCamelName }}:save")
async def {{ table.shortTableName }}_save(data: {{ table.tableHumpName }}Param = Body(description="{{ table.comment }}参数"), {{ table.shortTableName }}_service: {{ table.tableHumpName }}Service = Depends(get_{{ table.shortTableName }}_service)):
    with transactional_session({{ table.shortTableName }}_service.db):
        {{ table.shortTableName }}_service.save(data)
    return R.success()


@router.post("/{{ table.moduleName }}/{{ table.tableCamelName }}/update", summary="修改{{ table.comment }}", response_model=CommonResult, response_model_exclude_none=True)
@SaCheckPermission("{{ table.moduleName }}:{{ table.tableCamelName }}:update")
async def {{ table.shortTableName }}_update(data: {{ table.tableHumpName }}Param = Body(description="{{ table.comment }}参数"), {{ table.shortTableName }}_service: {{ table.tableHumpName }}Service = Depends(get_{{ table.shortTableName }}_service)):
    with transactional_session({{ table.shortTableName }}_service.db):
        {{ table.shortTableName }}_service.update(data)
    return R.success()


@router.post("/{{ table.moduleName }}/{{ table.tableCamelName }}/remove", summary="删除{{ table.comment }}", response_model=CommonResult, response_model_exclude_none=True)
@SaCheckPermission("{{ table.moduleName }}:{{ table.tableCamelName }}:remove")
async def {{ table.shortTableName }}_remove(param: IdsParam = Body(), {{ table.shortTableName }}_service: {{ table.tableHumpName }}Service = Depends(get_{{ table.shortTableName }}_service)):
    with transactional_session({{ table.shortTableName }}_service.db):
        {{ table.shortTableName }}_service.remove_by_ids(param.ids)
    return R.success()


@router.post("/{{ table.moduleName }}/{{ table.tableCamelName }}/detail", summary="{{ table.comment }}详情", response_model=CommonResult[{{ table.tableHumpName }}VO], response_model_exclude_none=True)
@SaCheckPermission(["{{ table.moduleName }}:{{ table.tableCamelName }}:detail", "{{ table.moduleName }}:{{ table.tableCamelName }}:update"], mode=SaMode.OR)
async def {{ table.shortTableName }}_detail(param: IdParam = Body(), {{ table.shortTableName }}_service: {{ table.tableHumpName }}Service = Depends(get_{{ table.shortTableName }}_service)):
    data = {{ table.shortTableName }}_service.detail(param.id)
    return R.data(data)
{% if table.treeTable %}

@router.post("/{{ table.moduleName }}/{{ table.tableCamelName }}/list", summary="{{ table.comment }}列表", response_model=CommonResult[List[{{ table.tableHumpName }}VO]], response_model_exclude_none=True)
@SaCheckPermission("{{ table.moduleName }}:{{ table.tableCamelName }}:list")
async def {{ table.shortTableName }}_list(param: {{ table.tableHumpName }}PageParam = Body(), {{ table.shortTableName }}_service: {{ table.tableHumpName }}Service = Depends(get_{{ table.shortTableName }}_service)):
    data = {{ table.shortTableName }}_service.list(param)
    return R.data(data)

@router.post("/{{ table.moduleName }}/{{ table.tableCamelName }}/tree", summary="{{ table.comment }}树", response_model=CommonResult[List[{{ table.tableHumpName }}VO]], response_model_exclude_none=True)
@SaCheckPermission("{{ table.moduleName }}:{{ table.tableCamelName }}:tree")
async def {{ table.shortTableName }}_tree(param: {{ table.tableHumpName }}PageParam = Body(), {{ table.shortTableName }}_service: {{ table.tableHumpName }}Service = Depends(get_{{ table.shortTableName }}_service)):
    data = {{ table.shortTableName }}_service.tree(param)
    return R.data(data)
{% else %}

@router.post("/{{ table.moduleName }}/{{ table.tableCamelName }}/page", summary="分页查询{{ table.comment }}列表", response_model=CommonResult[CommonPage[{{ table.tableHumpName }}VO]], response_model_exclude_none=True)
@SaCheckPermission("{{ table.moduleName }}:{{ table.tableCamelName }}:page")
async def {{ table.shortTableName }}_page(param: {{ table.tableHumpName }}PageParam = Body(), {{ table.shortTableName }}_service: {{ table.tableHumpName }}Service = Depends(get_{{ table.shortTableName }}_service)):
    data = {{ table.shortTableName }}_service.page(param)
    return R.data(data)
{% endif %}