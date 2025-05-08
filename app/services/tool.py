"""
工具服务层
"""

import logging

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError, BadRequestError
from app.models import Tool, ToolTag
from app.schemas.tool import ToolCreate, ToolUpdate
from app.services.tag import (
    STATUS_TO_INT,
    INT_TO_STATUS,
)

logger = logging.getLogger("app.services.tool")


def _tool_to_dict(db: Session, tool: Tool, include_status: bool = False) -> dict:
    result = {
        "id": tool.id,
        "name": tool.name,
        "description": tool.description,
        "url": tool.url,
        "icon": tool.icon,
        "category": tool.category,
    }
    if include_status:
        result["status"] = INT_TO_STATUS.get(tool.status, "draft")
    return result


# ── 查询 ──


def get_tools_paginated(
    db: Session, page: int, limit: int, search: str | None, tags: str | None
) -> dict:
    query = db.query(Tool).filter(Tool.status == 1)
    if search:
        like = f"%{search}%"
        query = query.filter((Tool.name.ilike(like)) | (Tool.description.ilike(like)))
    if tags:
        tag_list = [t.strip() for t in tags.split(",") if t.strip()]
        for tag_name in tag_list:
            # 按 category 过滤
            query = query.filter(Tool.category == tag_name)

    total = query.count()
    tools = query.offset((page - 1) * limit).limit(limit).all()
    return {
        "data": [_tool_to_dict(db, t) for t in tools],
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "pages": (total + limit - 1) // limit if limit > 0 else 0,
        },
    }


def get_tool_by_id(db: Session, tool_id: int) -> dict:
    tool = db.query(Tool).filter(Tool.id == tool_id, Tool.status == 1).first()
    if not tool:
        raise NotFoundError("工具")
    return _tool_to_dict(db, tool)


def get_all_tools_admin(db: Session) -> list[dict]:
    return [_tool_to_dict(db, t, include_status=True) for t in db.query(Tool).all()]


def get_all_tool_tags(db: Session) -> dict:
    """获取所有工具分类"""
    tools = db.query(Tool).filter(Tool.status == 1).all()
    categories = {}
    for t in tools:
        cat = t.category or "未分类"
        categories[cat] = categories.get(cat, 0) + 1
    return {"tags": [{"name": k, "count": v} for k, v in categories.items()]}


# ── 写入 ──


def create_tool(db: Session, data: ToolCreate) -> dict:
    tool = Tool(
        name=data.name,
        description=data.description,
        url=data.url,
        icon=data.icon,
        category=data.category,
        status=STATUS_TO_INT.get(data.status, 1),
    )
    db.add(tool)
    db.commit()
    db.refresh(tool)
    return {"message": "工具创建成功", "id": tool.id}


def update_tool(db: Session, tool_id: int, data: ToolUpdate) -> dict:
    tool = db.query(Tool).filter(Tool.id == tool_id).first()
    if not tool:
        raise NotFoundError("工具")

    if data.name is not None:
        tool.name = data.name
    if data.description is not None:
        tool.description = data.description
    if data.url is not None:
        tool.url = data.url
    if data.icon is not None:
        tool.icon = data.icon
    if data.category is not None:
        tool.category = data.category
    if data.status is not None and data.status in STATUS_TO_INT:
        tool.status = STATUS_TO_INT[data.status]

    db.commit()
    return {"message": "工具信息编辑成功", "id": tool.id, "name": tool.name}


def update_tool_status(db: Session, tool_id: int, status: str) -> dict:
    tool = db.query(Tool).filter(Tool.id == tool_id).first()
    if not tool:
        raise NotFoundError("工具")
    if status not in STATUS_TO_INT:
        raise BadRequestError("无效的状态值")
    tool.status = STATUS_TO_INT[status]
    db.commit()
    return {"message": "工具状态修改成功", "status": status}


def delete_tool(db: Session, tool_id: int) -> dict:
    tool = db.query(Tool).filter(Tool.id == tool_id).first()
    if not tool:
        raise NotFoundError("工具")
    db.query(ToolTag).filter(ToolTag.tool_id == tool_id).delete()
    db.delete(tool)
    db.commit()
    return {"message": "工具删除成功"}
