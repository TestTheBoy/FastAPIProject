from modules.sys.models.dept import Dept
from typing import List

from pydantic import Field


class DeptVO(Dept):
    children: List["DeptVO"] = Field(None, description="子部门")