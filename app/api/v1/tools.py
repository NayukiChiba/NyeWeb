"""
工具 API 路由
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.tool import ToolCreate, ToolUpdate
from app.services import tool as tool_service

router = APIRouter()


@router.get("/tools")
def get_tools(
    page: int = 1,
    limit: int = 6,
    search: str = None,
    tags: str = None,
    db: Session = Depends(get_db),
):
    return tool_service.get_tools_paginated(db, page, limit, search, tags)


@router.get("/tool-tags")
def get_all_tool_tags(db: Session = Depends(get_db)):
    return tool_service.get_all_tool_tags(db)


@router.get("/admin/tools")
def get_all_tools_admin(db: Session = Depends(get_db)):
    return tool_service.get_all_tools_admin(db)


@router.get("/tools/{tool_id}")
def get_tool_by_id(tool_id: int, db: Session = Depends(get_db)):
    return tool_service.get_tool_by_id(db, tool_id)


@router.post("/tools")
def create_tool(data: ToolCreate, db: Session = Depends(get_db)):
    return tool_service.create_tool(db, data)


@router.put("/tools/{tool_id}")
def update_tool(tool_id: int, data: ToolUpdate, db: Session = Depends(get_db)):
    return tool_service.update_tool(db, tool_id, data)


@router.patch("/tools/{tool_id}/status")
def update_tool_status(tool_id: int, status_data: dict, db: Session = Depends(get_db)):
    return tool_service.update_tool_status(db, tool_id, status_data.get("status"))


@router.delete("/tools/{tool_id}")
def delete_tool(tool_id: int, db: Session = Depends(get_db)):
    return tool_service.delete_tool(db, tool_id)
