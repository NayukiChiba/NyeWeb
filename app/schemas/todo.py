"""
待办事项 Pydantic Schema
"""

from pydantic import BaseModel


class TodoCreate(BaseModel):
    task: str
    priority: str = "medium"
    type: str = "short-term"
    progress: int = 0
    icon: str | None = None
    status: str = "active"


class TodoUpdate(BaseModel):
    task: str | None = None
    completed: bool | None = None
    priority: str | None = None
    type: str | None = None
    progress: int | None = None
    icon: str | None = None
    status: str | None = None


class TodoResponse(BaseModel):
    id: int
    task: str
    completed: bool = False
    priority: str = "medium"
    type: str = "short-term"
    progress: int = 0
    icon: str | None = None
    status: str = "active"

    model_config = {"from_attributes": True}
