from pydantic import BaseModel,Field
from typing import Optional



class LoginParam(BaseModel):
    #使用 alias，允许前端传 userName，后端接收为 username
    username: Optional[str] = Field(..., title="用户名", description="用户名",alias="userName")
    password: Optional[str] = Field(..., title="密码", description="密码")
    # 允许通过别名或原始名称填充
    class Config:
        populate_by_name = True