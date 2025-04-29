"""
时间线 ORM 模型
"""

from sqlalchemy import Column, Integer, Text, DateTime

from app.core.database import Base


class Timeline(Base):
    __tablename__ = "timeline"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, nullable=False)
    content = Column(Text, nullable=False)
