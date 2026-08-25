from modules.{{ table.moduleName }}.models.{{ table.shortTableName }} import {{ table.tableHumpName }}
{% if table.treeTable %}from typing import List

from pydantic import Field{% endif %}


class {{ table.tableHumpName }}VO({{ table.tableHumpName }}):{% if table.treeTable %}
    children: List["{{ table.tableHumpName }}VO"] = Field(None, description="子{{ table.comment|replace("表", "") }}"){% else %}
    pass{% endif %}