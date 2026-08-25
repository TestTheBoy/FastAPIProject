
from typing import Union
from pydantic import BaseModel, Field
from modules.sys.models.dict import Dict



class DictVO(Dict):
    pass

class LabelValueVO(BaseModel):
    label: str = Field(..., title="标签", description="标签")
    value: Union[str,int] = Field(..., title="值", description="值")
    ext: dict = Field({}, title="扩展信息", description="扩展信息")