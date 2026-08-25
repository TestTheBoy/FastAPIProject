#创建数据库引擎
import os
from contextlib import contextmanager

import redis
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

#构建数据库URL
mysql_url = "localhost"
DB_PASSWORD = "123qwe"
DB_USER = "root"
DB_NAME = "sys"
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@localhost:3306/{DB_NAME}?charset=utf8mb4"

#获取数据库引擎选项
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# 会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db(app=None):
    """
    初始化数据库连接（创建表等）

    在应用启动时调用，确保数据库引擎已就绪。
    如需自动建表，可在此处调用 Base.metadata.create_all(engine)。
    """
    # 验证数据库连接可用
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception as e:
        raise RuntimeError(f"数据库连接失败: {e}")


def get_redis() -> redis.Redis:
    """
    获取 Redis 客户端实例

    从环境变量读取 Redis 连接参数，返回配置好的 Redis 客户端。
    """
    host = os.environ.get("REDIS_HOST", "localhost")
    port = int(os.environ.get("REDIS_PORT", "6379"))
    password = os.environ.get("REDIS_PASSWORD", "")
    db = int(os.environ.get("REDIS_DB", "0"))

    client = redis.Redis(
        host=host,
        port=port,
        password=password or None,
        db=db,
        decode_responses=False,
    )
    return client

# def create_db_and_tables():
#     """
#     创建数据库和表
#     """
#     SQLModel.metadata.create_all(engine)

def get_session():
    """
    获取数据库会话
    """
    with Session(engine) as session:
        yield session

    if __name__ == "__main__":
        session:Session = get_session()
        session.exec("select * from sys_user")

@contextmanager
def transactional_session(db: Session):
    """事务性会话上下文管理器"""
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        raise e