"""
收藏图片 ORM 模型
"""

from sqlalchemy import Column, Integer, String

from app.core.database import Base


class FavoriteImage(Base):
    __tablename__ = "favorite_images"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(2083), nullable=False)
