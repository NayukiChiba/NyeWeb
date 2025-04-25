"""
项目 ORM 模型 — 链接形式
"""

from sqlalchemy import Column, Integer, SmallInteger, String, Text, JSON

from app.core.database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    link = Column(String(2083), nullable=False)  # GitHub 链接
    tech_stack = Column(JSON, default=list)  # 技术栈 ["Python", "Vue"]
    status = Column(String(50), default="planning")  # planning/in-progress/completed
    visibility = Column(SmallInteger, nullable=False, default=1)  # 0=draft 1=published
