"""
日记 ORM 模型
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, JSON

from app.core.database import Base


class Diary(Base):
    __tablename__ = "diaries"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, nullable=False)
    content = Column(Text, nullable=False)
    mood = Column(String(50))  # happy/tired/neutral/excited
    weather = Column(String(50))  # sunny/cloudy/rainy
    images = Column(JSON, default=list)  # 图片 URL 列表
