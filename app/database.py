import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# sessionmaker：生成数据库会话（Session）的工厂。

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
# DATABASE_URL：数据库连接字符串，格式通常为： "数据库类型://用户名:密码@主机:端口/数据库名"


engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
# create_engine：创建核心接口，用于管理数据库连接池。
# echo=True：调试模式下打印所有执行的 SQL 语句（生产环境应设为 False）。

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# autocommit=False：禁用自动提交（需显式调用 commit()）。
# autoflush=False：禁用自动刷新（避免意外刷新未完成的操作）。
# bind=engine：绑定到之前创建的引擎。

Base = declarative_base()

# 作用：为每个请求生成独立的数据库会话，并在请求结束后自动关闭。
def get_db():
    db = SessionLocal()
    try:
        yield db # yield db：将会话提供给路由函数使用
    finally:
        db.close()