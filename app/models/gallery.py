"""
图库 ORM 模型
"""

from sqlalchemy import Column, Integer, SmallInteger, String, Date, JSON

from app.core.database import Base


class Gallery(Base):
    __tablename__ = "gallery"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    url = Column(String(2083), nullable=False)
    date = Column(Date)
    tags = Column(JSON, default=list)  # 标签列表 ["wife", "wallpaper"]
    status = Column(SmallInteger, nullable=False, default=1)
