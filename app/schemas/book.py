"""
书籍 Pydantic Schema
"""

from pydantic import BaseModel


class BookCreate(BaseModel):
    title: str
    url: str
    description: str | None = None
    cover: str | None = None
    tags: list[str] | None = None
    status: str = "draft"


class BookUpdate(BaseModel):
    title: str | None = None
    url: str | None = None
    description: str | None = None
    cover: str | None = None
    tags: list[str] | None = None
    status: str | None = None


class BookResponse(BaseModel):
    id: int
    title: str
    url: str
    description: str | None = None
    cover: str | None = None
    tags: list[str] = []


class BookAdminResponse(BookResponse):
    status: str = "draft"
