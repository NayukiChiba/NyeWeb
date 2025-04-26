"""
书籍 ORM 模型
"""

from sqlalchemy import Column, Integer, SmallInteger, String, Text

from app.core.database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    cover = Column(String(500))
    url = Column(String(2083), nullable=False)  # 下载/阅读链接
    status = Column(SmallInteger, nullable=False, default=1)
