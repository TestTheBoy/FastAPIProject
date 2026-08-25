from modules.sys.models.menu import Menu
from typing import List

from pydantic import Field


class MenuVO(Menu):
    children: List["MenuVO"] = Field(None, description="子菜单")
    disabled: bool = Field(False, description="禁用")