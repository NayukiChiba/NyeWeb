"""
工具 ORM 模型
"""

from sqlalchemy import Column, Integer, SmallInteger, String, Text

from app.core.database import Base


class Tool(Base):
    __tablename__ = "tools"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    url = Column(String(2083))
    icon = Column(Text)  # SVG 图标
    category = Column(String(100))  # 分类: AI/API/前端/服务器/资源/...
    status = Column(SmallInteger, nullable=False, default=1)
