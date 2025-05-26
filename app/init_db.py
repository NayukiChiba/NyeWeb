"""
数据库初始化脚本 — 创建表和管理员账户
"""

import logging

from app.core.config import get_settings
from app.core.database import engine, SessionLocal
from app.models import Base, Admin
from app.services.admin import create_admin

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("init_db")


def create_database_tables() -> None:
    """创建所有数据库表"""
    Base.metadata.create_all(bind=engine)
    logger.info("数据库表创建成功!")


def create_admin_account() -> None:
    """创建管理员账户"""
    settings = get_settings()
    if not settings.ADMIN_PASSWORD:
        logger.warning("ADMIN_PASSWORD 未设置，跳过管理员账户创建")
        return

    db = SessionLocal()
    try:
        existing = db.query(Admin).filter(Admin.username == "admin").first()
        if not existing:
            create_admin(db, "admin", settings.ADMIN_PASSWORD)
            logger.info("管理员账户创建成功!")
        else:
            logger.info("管理员账户已存在!")
    finally:
        db.close()


def init_database() -> None:
    """初始化数据库"""
    create_database_tables()
    create_admin_account()


if __name__ == "__main__":
    init_database()
