"""
文章 ORM 模型
"""

from sqlalchemy import Column, Integer, SmallInteger, String, Text, Date, DateTime

from app.core.database import Base


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False, unique=True)
    category = Column(String(100))
    date = Column(Date)
    description = Column(Text)  # 文章描述/摘要
    image = Column(String(2083))  # 封面图 URL
    word_count = Column(Integer, default=0)  # 字数统计
    updated_at = Column(DateTime)  # 最后更新时间
    status = Column(SmallInteger, nullable=False, default=1)
