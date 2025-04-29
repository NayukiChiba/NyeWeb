"""
管理员 ORM 模型
"""

from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from app.core.database import Base


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    password_hash = Column(String(128))
    created_at = Column(DateTime, default=datetime.utcnow)
