"""
工具 Pydantic Schema
"""

from pydantic import BaseModel


class ToolCreate(BaseModel):
    name: str
    description: str | None = None
    url: str | None = None
    icon: str | None = None
    category: str | None = None
    status: str = "published"


class ToolUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    url: str | None = None
    icon: str | None = None
    category: str | None = None
    status: str | None = None


class ToolResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    url: str | None = None
    icon: str | None = None
    category: str | None = None

    model_config = {"from_attributes": True}


class ToolAdminResponse(ToolResponse):
    status: str = "draft"
