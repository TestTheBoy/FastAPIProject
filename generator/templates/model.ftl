{% if table.need_decimal %}
from decimal import Decimal{% endif %}
from App_Demo.db_types import db_types
from pydantic import Field
from App_Demo.base import APIModel
from App_Demo.base import BaseOrmModel
{% if table.need_datetime %}
from datetime import datetime
{% endif %}{% if table.need_optional %}
from typing import Optional
{% endif %}

# 数据库模型
class {{ table.tableHumpName }}OrmModel(BaseOrmModel):
    """
    {{ table.comment }}数据库模型
    """
    __tablename__ = '{{ table.tableName }}'
    
    # 如果数据库中不存在基类字段，则设置为None（不映射到数据库列）
    {%- set base_fields = {'id':'id', 'create_time':'createTime', 'update_time':'updateTime', 'create_user':'createUser', 'update_user':'updateUser', 'is_deleted':'isDeleted'} %}
    {%- for field_db_name, field_model_name in base_fields.items() %}
        {%- set field_exists = [] %}
        {%- for column in table.columns %}
            {%- if column.name == field_db_name %}
                {%- set _ = field_exists.append(1) %}
            {%- endif %}
        {%- endfor %}
        {%- if field_exists|length == 0 %}
    {{ field_model_name }} = None
        {%- endif %}
    {%- endfor %}
    
    # SQLAlchemy字段定义
    {%- for column in table.columns %}
        {%- if column.name not in base_fields.keys() %}
    {{ column.camelName }}: {% if column.type == 'String' %}str{% elif column.type == 'Integer' %}int{% elif column.type == 'BigInteger' %}str{% elif column.type == 'DateTime' %}datetime{% elif column.type == 'Numeric' %}Decimal{% else %}str{% endif %} = db_types.Column({% if column.type == 'String' %}db_types.String({{ column.length }}){% elif column.type == 'Integer' %}db_types.Integer{% elif column.type == 'BigInteger' %}db_types.BigInteger{% elif column.type == 'DateTime' %}db_types.DateTime{% elif column.type == 'Numeric' %}db_types.Numeric({{ column.precision }}, {{ column.scale }}){% else %}db_types.String({{ column.length if column.length else 255 }}){% endif %}, name="{{ column.name }}"{% if column.nullable %}, nullable=True{% else %}, nullable=False{% endif %}{% if column.primaryKey %}, primary_key=True{% endif %}{% if column.autoincrement %}, autoincrement=True{% endif %}, comment="{{ column.comment }}")
        {%- endif %}
    {%- endfor %}

# Pydantic模型
class {{ table.tableHumpName }}(APIModel):
    """
    {{ table.comment }}Pydantic模型，用于API接口
    """
    # Pydantic字段定义
    {%- for column in table.columns %}
        {%- if column.name not in base_fields.keys() %}
    {{ column.camelName }}: {% if column.nullable %}Optional[{% endif %}{% if column.type == 'String' %}str{% elif column.type == 'Integer' %}int{% elif column.type == 'BigInteger' %}str{% elif column.type == 'DateTime' %}datetime{% elif column.type == 'Numeric' %}Decimal{% else %}str{% endif %}{% if column.nullable %}]{% endif %} = Field(None, description="{{ column.comment }}")
        {%- endif %}
    {%- endfor %}