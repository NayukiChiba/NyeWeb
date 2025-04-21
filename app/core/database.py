"""
数据库引擎、Session 工厂、依赖注入
"""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase

from app.core.config import get_settings


class Base(DeclarativeBase):
    """ORM 模型基类"""

    pass


settings = get_settings()
engine = create_engine(settings.DATABASE_URL, echo=settings.DEBUG, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """FastAPI 依赖注入 — 提供数据库 Session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
