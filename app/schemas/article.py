"""
文章 Pydantic Schema
"""

from pydantic import BaseModel


class ArticleCreate(BaseModel):
    title: str
    content: str
    slug: str | None = None
    description: str | None = None
    category: str | None = None
    image: str | None = None
    date: str | None = None
    tags: list[str] | None = None
    status: str = "draft"


class ArticleUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    description: str | None = None
    category: str | None = None
    image: str | None = None
    date: str | None = None
    tags: list[str] | None = None
    status: str | None = None


class ArticleResponse(BaseModel):
    id: int
    title: str
    slug: str
    description: str | None = None
    category: str | None = None
    image: str | None = None
    date: str | None = None
    word_count: int = 0
    tags: list[str] = []


class ArticleAdminResponse(ArticleResponse):
    status: str = "draft"
    updated_at: str | None = None


class CategoryCreate(BaseModel):
    name: str
    path: str | None = None
    parent: str | None = None
