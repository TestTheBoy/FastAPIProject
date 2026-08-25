from typing import List, Optional

from pydantic import BaseModel, Field
from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

from App_Demo.base import R, CommonPage, CommonResult, BasePageParam
from database import get_session

router = APIRouter(tags=["消息中心"])


class MessagePageParam(BasePageParam):
    m_EQ_isRead: Optional[int] = None


class MessageVO(BaseModel):
    id: str
    title: str
    content: str
    isRead: int = 0


def get_message_service(db: Session = Depends(get_session)):
    return db


@router.post("/sys/message/page", summary="消息分页", response_model=CommonResult[CommonPage[MessageVO]], response_model_exclude_none=True)
async def message_page(param: MessagePageParam = Body(), db: Session = Depends(get_session)):
    rows = [
        MessageVO(id="1", title="欢迎", content="欢迎使用系统", isRead=0),
        MessageVO(id="2", title="提示", content="请及时查看消息", isRead=1),
    ]
    if param.m_EQ_isRead is not None:
        rows = [row for row in rows if row.isRead == param.m_EQ_isRead]

    page = CommonPage[MessageVO](
        recordCount=len(rows),
        totalPage=1 if rows else 0,
        pageSize=param.pageSize,
        pageNum=param.pageNum,
        rows=rows[:param.pageSize],
    )
    return R.data(page)
