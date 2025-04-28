"""
待办事项 ORM 模型
"""

from sqlalchemy import Column, Integer, String, Text, Boolean

from app.core.database import Base


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    task = Column(String(500), nullable=False)
    completed = Column(Boolean, default=False)
    priority = Column(String(50), default="medium")  # high/medium/low
    type = Column(String(50), default="short-term")  # short-term/mid-term/long-term
    progress = Column(Integer, default=0)  # 0-100
    icon = Column(Text)  # SVG 图标
    status = Column(String(50), default="active")  # active/completed
