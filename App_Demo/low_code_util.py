'''
通用查询构建工具类,通过解析前端传来的特定格式参数，自动拼凑出 SQLAlchemy 的数据库查询语句，并处理一些通用的业务逻辑（如分页、排序、唯一性校验等）
'''

import importlib
import logging
from typing import Any, List, Optional

from sqlalchemy import text
from App_Demo.base import BaseOrmModel, BasePageParam
from sqlalchemy.orm import Query, Session

from App_Demo.core.exception import AssertTool
from App_Demo.query_param_context import QueryParamContext
# from App_Demo.exception import AssertTool
from App_Demo.util import StrUtil
from modules.sys.vos.dict_vo import LabelValueVO


class LowCodeUtil:
    @staticmethod
    def build_query(page_param: BasePageParam, model: BaseOrmModel, db: Session, query: Optional[Query]) -> Query:
        """
        构建查询条件
        :param page_param: 分页查询对象
        :param model: 查询模型
        :param db: 数据库会话
        :return: SQLAlchemy查询对象
        """
        query_param = QueryParamContext.get_query_param()
        if query is None:
            query = db.query(model)

        query_param.update(page_param.model_dump(mode='python'))
        table_alias = None
        
        for key, value in query_param.items():
            if value and key.startswith('m_'):
                parts = key.split('_')  # 拆分所有部分
                if len(parts) < 3:
                    continue

                # 解析参数格式
                if len(parts) == 3:
                    # 格式: ['m', '操作符', '字段名']
                    _, operator, field_name = parts
                elif len(parts) >= 4:
                    # 格式: ['m', '表别名', '操作符', '字段名']
                    _, table_alias, operator, field_name = parts[:4]
                    # 如果还有更多部分，将其余部分合并到字段名中
                    if len(parts) > 4:
                        field_name = '_'.join(parts[3:])
                else:
                    continue

                # 获取字段引用
                field = None
                if hasattr(model, field_name):
                    field = getattr(model, field_name)
                if table_alias:
                    field_name = StrUtil.hump_to_underline(field_name)
                # 应用不同的操作符
                if operator == 'EQ':
                    # 等于=
                    if table_alias:
                        paramName = f'{table_alias}_{field_name}'
                        query = query.filter(text(f'{table_alias}.{field_name} = :{paramName}')).params(
                            **{paramName: value})
                    else:
                        query = query.filter(field == value)
                elif operator == 'NE':
                    # 不等于<>
                    if table_alias:
                        paramName = f'{table_alias}_{field_name}'
                        query = query.filter(text(f'{table_alias}.{field_name} <> :{paramName}')).params(
                            **{paramName: value})
                    else:
                        query = query.filter(field != value)
                elif operator == 'GT':
                    # 大于>
                    if table_alias:
                        paramName = f'{table_alias}_{field_name}'
                        query = query.filter(text(f'{table_alias}.{field_name} > :{paramName}')).params(
                            **{paramName: value})
                    else:
                        query = query.filter(field > value)
                elif operator == 'GE':
                    # 大于等于>=
                    if table_alias:
                        paramName = f'{table_alias}_{field_name}'
                        query = query.filter(text(f'{table_alias}.{field_name} >= :{paramName}')).params(
                            **{paramName: value})
                    else:
                        query = query.filter(field >= value)
                elif operator == 'LT':
                    # 小于<
                    if table_alias:
                        paramName = f'{table_alias}_{field_name}'
                        query = query.filter(text(f'{table_alias}.{field_name} < :{paramName}')).params(
                            **{paramName: value})
                    else:
                        query = query.filter(field < value)
                elif operator == 'LE':
                    # 小于等于<=
                    if table_alias:
                        paramName = f'{table_alias}_{field_name}'
                        query = query.filter(text(f'{table_alias}.{field_name} <= :{paramName}')).params(
                            **{paramName: value})
                    else:
                        query = query.filter(field <= value)
                elif operator == 'BT':
                    # between 值1 and 值2
                    if isinstance(value, (list, tuple)) and len(value) == 2:
                        if table_alias:
                            paramName1 = f'{table_alias}_{field_name}1'
                            paramName2 = f'{table_alias}_{field_name}2'
                            query = query.filter(
                                text(f'{table_alias}.{field_name} between :{paramName1} and :{paramName2}')).params(
                                **{paramName1: value[0], paramName2: value[1]})
                        else:
                            query = query.filter(field.between(value[0], value[1]))
                elif operator == 'LIKE':
                    # like '%值%'
                    if table_alias:
                        paramName = f'{table_alias}_{field_name}'
                        query = query.filter(text(f'{table_alias}.{field_name} LIKE :{paramName}')).params(
                            **{paramName: f'%{value}%'})
                    else:
                        query = query.filter(field.like(f'%{value}%'))
                elif operator == 'NLIKE':
                    # not like '%值%'
                    if table_alias:
                        paramName = f'{table_alias}_{field_name}'
                        query = query.filter(text(f'{table_alias}.{field_name} NOT LIKE :{paramName}')).params(
                            **{paramName: f'%{value}%'})
                    else:
                        query = query.filter(~field.like(f'%{value}%'))
                elif operator == 'LLIKE':
                    # like '%abc'
                    if table_alias:
                        paramName = f'{table_alias}_{field_name}'
                        query = query.filter(text(f'{table_alias}.{field_name} LIKE :{paramName}')).params(
                            **{paramName: f'%{value}'})
                    else:
                        query = query.filter(field.like(f'%{value}'))
                elif operator == 'RLIKE':
                    # like 'abc%'
                    if table_alias:
                        paramName = f'{table_alias}_{field_name}'
                        query = query.filter(text(f'{table_alias}.{field_name} LIKE :{paramName}')).params(
                            **{paramName: f'{value}%'})
                    else:
                        query = query.filter(field.like(f'{value}%'))
                elif operator == 'IN':
                    # in(值1,值2)
                    if table_alias:
                        paramName = f'{table_alias}_{field_name}'
                        # 构造IN语句的占位符
                        placeholders = ', '.join([f':{paramName}_{i}' for i in range(len(value))])
                        params = {f'{paramName}_{i}': v for i, v in enumerate(value)}
                        query = query.filter(text(f'{table_alias}.{field_name} IN ({placeholders})')).params(**params)
                    else:
                        query = query.filter(field.in_(value))
                elif operator == 'NIN':
                    # not in(值1,值2)
                    if table_alias:
                        paramName = f'{table_alias}_{field_name}'
                        # 构造NOT IN语句的占位符
                        placeholders = ', '.join([f':{paramName}_{i}' for i in range(len(value))])
                        params = {f'{paramName}_{i}': v for i, v in enumerate(value)}
                        query = query.filter(text(f'{table_alias}.{field_name} NOT IN ({placeholders})')).params(
                            **params)
                    else:
                        query = query.filter(~field.in_(value))
        # 处理includeIds和includeType的逻辑
        if page_param.includeIds and page_param.includeType == 2:
            placeholders = ', '.join([f':id_{i}' for i in range(len(page_param.includeIds))])
            params = {f'id_{i}': v for i, v in enumerate(page_param.includeIds)}
            query = query.filter(text(f'id IN ({placeholders})')).params(**params)
        # 处理keywords和searchKeys
        if page_param.keywords and page_param.searchKeys:
            if table_alias:
                # 使用表别名构建关键字查询
                search_keys = page_param.searchKeys.split(',')
                conditions = []
                for i, key in enumerate(search_keys):
                    key = key.strip()
                    if key:
                        param_name = f'{table_alias}_{key}_keywords'
                        conditions.append(text(f'{table_alias}.{key} LIKE :{param_name}'))
                        query = query.params(**{param_name: f'%{page_param.keywords}%'})
                if conditions:
                    # 使用or_连接所有条件
                    from sqlalchemy import or_
                    query = query.filter(or_(*conditions))
            else:
                # 不使用表别名构建关键字查询
                search_keys = page_param.searchKeys.split(',')
                conditions = []
                for key in search_keys:
                    key = key.strip()
                    if key and hasattr(model, key):
                        field = getattr(model, key)
                        conditions.append(field.like(f'%{page_param.keywords}%'))
                if conditions:
                    # 使用or_连接所有条件
                    from sqlalchemy import or_
                    query = query.filter(or_(*conditions))
        # 处理排序orderBy
        # t.id ASC,t.name DESC或者id ASC,name DESC
        if page_param.orderBy:
            order_parts = page_param.orderBy.split(',')
            for part in order_parts:
                part = part.strip()
                if ' ' in part:
                    field_part, direction = part.rsplit(' ', 1)
                    direction = direction.upper()

                    # 处理带表别名的情况 t.id 或者单独字段名 id
                    if '.' in field_part:
                        alias, field_name = field_part.split('.', 1)
                        # 使用表别名
                        field_name = StrUtil.hump_to_underline(field_name)
                        if direction == 'DESC':
                            query = query.order_by(text(f'{alias}.{field_name} DESC'))
                        else:
                            query = query.order_by(text(f'{alias}.{field_name} ASC'))
                    else:
                        # 不带表别名
                        field_name = field_part
                        if hasattr(model, field_name):
                            field = getattr(model, field_name)
                            if direction == 'DESC':
                                query = query.order_by(field.desc())
                            else:
                                query = query.order_by(field.asc())
        # 在这里还可以处理，数据权限或才逻辑删除等
        if model and hasattr(model, 'isDeleted') and getattr(model, 'isDeleted') is not None:
            query = query.filter(model.isDeleted == 0)
        return query

    @staticmethod
    def select(moduleName: str, tableName: str, param: BasePageParam, db: Session, callSelect: bool = False,
               voList: List[Any] = []):
        """
        通用下拉
        :param moduleName: 模块名称
        :param tableName: 表名称
        :param param: 查询参数
        :param db: 数据库会话
        :param callSelect: 是否调用select方法
        :param voList: vo列表
        """
        # 使用通用下拉处理
        param.pageSize = 5000
        # 获取模块服务类字符串
        try:
            if not voList:
                module: str = f"modules.{moduleName}.services.{StrUtil.hump_to_underline(tableName)}_service"
                # 动态导入模块服务类
                moduleObj = importlib.import_module(module)
                ServiceClass = getattr(moduleObj, StrUtil.camel_to_hump(tableName) + "Service")
                # 获取模块服务类
                service = ServiceClass(db)
                if callSelect and hasattr(service, 'select'):
                    return service.select(param)
                else:
                    datas: List[Any] = service.list(param)
            else:
                datas = voList
            # 在这里处理includeIds和includeType==1的逻辑
            # ===>指定追加指定ID的数据
            if param.includeIds and param.includeType == 1:
                allIds: List[str] = []
                for data in datas:
                    allIds.append(data.id)
                for includeId in param.includeIds:
                    if includeId not in allIds:
                        newData = service.detail(includeId)
                        if newData:
                            datas.insert(0, newData)
            return LowCodeUtil.vos_to_lvs(datas, param)
        except Exception as e:
            logging.error(e)
            return []

    @staticmethod
    def vos_to_lvs(voList: List[Any], param: BasePageParam) -> List[LabelValueVO]:
        """
        vo列表转成LabelValueVO列表
        :param voList: vo列表
        :param param: 查询参数
        :return: LabelValueVO列表
        """
        res: List[LabelValueVO] = []
        for vo in voList:
            if hasattr(vo, param.labelKey) and hasattr(vo, param.valueKey):
                lv: LabelValueVO = LabelValueVO(label=getattr(vo, param.labelKey), value=getattr(vo, param.valueKey))
                if param.extFieldNames:
                    extFieldNameList = param.extFieldNames.split(',')
                    for fieldName in extFieldNameList:
                        if hasattr(vo, fieldName):
                            lv.ext[fieldName] = getattr(vo, fieldName)
                res.append(lv)
        return res

    @staticmethod
    def check_unique(model_query: Query, column: str, value: Any, id_value: Any, error_msg: str):
        """
        校验唯一性
        :param model_query: 数据库模型查询对象
        :param column: 列名(支持表别名)
        :param value: 要校验的值
        :param id_value: 当前记录ID(更新时使用)
        :param error_msg: 不唯一时的错误信息
        :return: 如果不唯一返回异常，否则返回None
        """
        # 构建查询条件
        column = StrUtil.hump_to_underline(column)
        # 检查模型是否有指定的列
        query = model_query.filter(text(f"{column} = :value")).params(value=value)

        # 如果是更新操作，排除当前记录
        if id_value is not None:
            query = query.filter(text("id != :id")).params(id=id_value)
        if 'is_deleted' in str(query):
            query = query.filter(text("is_deleted = :is_deleted_param")).params(is_deleted_param=0)
        # 执行查询
        count = query.count()
        # 如果不唯一则抛出错误
        if count > 0:
            AssertTool.raise_biz_with_msg(error_msg)
