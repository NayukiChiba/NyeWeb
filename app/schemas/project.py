"""
项目 Pydantic Schema — 链接形式
"""

from pydantic import BaseModel


class ProjectCreate(BaseModel):
    name: str
    link: str
    description: str | None = None
    tech_stack: list[str] | None = None
    status: str = "planning"  # planning/in-progress/completed
    visibility: str = "draft"  # draft/published


class ProjectUpdate(BaseModel):
    name: str | None = None
    link: str | None = None
    description: str | None = None
    tech_stack: list[str] | None = None
    status: str | None = None
    visibility: str | None = None


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    link: str
    tech_stack: list[str] = []
    status: str = "planning"


class ProjectAdminResponse(ProjectResponse):
    visibility: str = "draft"
