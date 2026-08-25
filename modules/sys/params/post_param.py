from pydantic import BaseModel, Field
from typing import Optional


from App_Demo.base import BasePageParam


class PostParam(BaseModel):
    id: Optional[str] = Field(None, title="主键", description="主键")

    
    
    name: str = Field(..., title="岗位名称", description="岗位名称")
    
    code: str = Field(..., title="唯一编码", description="唯一编码")
    
    sort: int = Field(None, title="排序", description="排序")
    
    enabled: Optional[int] = Field(None, title="是否启用", description="是否启用")
    
    remark: Optional[str] = Field(None, title="备注", description="备注")
    
    
    
    
    
    


class PostPageParam(BasePageParam):
    pass