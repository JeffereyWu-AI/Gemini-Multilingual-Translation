# 定义三个数据库模型，并创建了对应的数据库表

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, create_engine
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

Base = declarative_base()

# 记录用户提交的翻译请求，包括原文、目标语言和状态
class TranslationRequest(Base):
    __tablename__ = "translation_requests"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    languages = Column(String, nullable=False)
    status = Column(String, default="in progress", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# 存储每个请求的翻译结果（按语言拆分）
# 一个TranslationRequest可以对应多个TranslationResult
class TranslationResult(Base):
    __tablename__ = "translation_results"
    id = Column(Integer, primary_key=True, index=True)
    # request_id: 外键，关联到TranslationRequest表的id
    request_id = Column(Integer, ForeignKey("translation_requests.id"), nullable=False)
    language = Column(String, nullable=False)
    translated_text = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class IndividualTranslations(Base):
    __tablename__ = "individual_translations"
    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("translation_requests.id"), nullable=False)
    translated_text = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# to ensure tables are created in the database
engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base.metadata.create_all(engine) # 在数据库中生成所有定义的表