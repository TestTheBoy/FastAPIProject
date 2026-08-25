import logging
from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


class VisLogService:
    """
    访问日志服务
    用于记录登录、登出、扮演用户等操作的访问日志
    """

    def __init__(self, db: Optional[Session] = None):
        self.db = db

    def save_vis_log(
        self,
        visType: str,
        account: str = "unknown",
        success: str = "Y",
        message: str = "",
        ip: str = "",
        userId: Optional[str] = None,
    ) -> bool:
        """
        保存访问日志

        :param visType: 访问类型，参考 VisTypeEnum
        :param account: 账号
        :param success: 是否成功 Y/N
        :param message: 日志消息
        :param ip: 客户端IP
        :param userId: 用户ID
        :return: 是否保存成功
        """
        log_entry = (
            f"[VisLog] type={visType}, account={account}, "
            f"success={success}, message={message}, "
            f"ip={ip}, userId={userId}, "
            f"time={datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        logger.info(log_entry)

        # TODO: 后续接入 vis_log 数据库表后，取消下面注释
        # from modules.sys.models.vis_log import VisLogOrmModel
        # model = VisLogOrmModel(
        #     visType=visType,
        #     account=account,
        #     success=success,
        #     message=message,
        #     ip=ip,
        #     userId=userId,
        # )
        # self.db.add(model)
        # self.db.flush()

        return True
