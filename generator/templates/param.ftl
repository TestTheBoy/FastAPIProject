from pydantic import BaseModel, Field
from typing import Optional{% if table.need_union %},Union{% endif %}
{% if table.need_decimal %}
from decimal import Decimal
{% endif %}

from App_Demo.base import BasePageParam


class {{ table.tableHumpName }}Param(BaseModel):
    id: Optional[str] = Field(None, title="主键", description="主键")

    {% for column in table.columns %}
    {%- if column.name not in ['id', 'create_time', 'update_time', 'create_user', 'update_user', 'is_deleted'] %}
    {{ column.camelName }}: {% if column.nullable %}Optional[{% endif %}{% if column.type == 'String' %}str{% elif column.type == 'Integer' %}int{% elif column.type == 'BigInteger' %}str{% elif column.type == 'DateTime' %}str{% elif column.type == 'Numeric' %}Decimal{% else %}str{% endif %}{% if column.nullable %}]{% endif %} = Field({% if column.nullable %}None{% else %}...{% endif %}, title="{{ column.comment }}", description="{{ column.comment }}")
    {%- endif %}
    {% endfor %}


class {{ table.tableHumpName }}PageParam(BasePageParam):
    pass