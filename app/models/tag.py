"""
标签 ORM 模型 + 所有关联表
"""

from sqlalchemy import Column, Integer, String, ForeignKey

from app.core.database import Base


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)


class ArticleTag(Base):
    __tablename__ = "article_tags"

    article_id = Column(Integer, ForeignKey("articles.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)


class ProjectTag(Base):
    __tablename__ = "project_tags"

    project_id = Column(Integer, ForeignKey("projects.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)


class BookTag(Base):
    __tablename__ = "book_tags"

    book_id = Column(Integer, ForeignKey("books.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)


class ToolTag(Base):
    __tablename__ = "tool_tags"

    tool_id = Column(Integer, ForeignKey("tools.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)
