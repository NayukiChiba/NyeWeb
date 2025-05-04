"""
图库 Pydantic Schema
"""

from pydantic import BaseModel


class GalleryCreate(BaseModel):
    title: str
    url: str
    date: str | None = None
    tags: list[str] | None = None
    status: str = "published"


class GalleryUpdate(BaseModel):
    title: str | None = None
    url: str | None = None
    date: str | None = None
    tags: list[str] | None = None
    status: str | None = None


class GalleryResponse(BaseModel):
    id: int
    title: str
    url: str
    date: str | None = None
    tags: list[str] = []
    status: str = "published"

    model_config = {"from_attributes": True}
