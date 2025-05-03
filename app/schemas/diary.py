"""
日记 Pydantic Schema
"""

from pydantic import BaseModel


class DiaryCreate(BaseModel):
    date: str
    content: str
    mood: str | None = None
    weather: str | None = None
    images: list[str] | None = None


class DiaryUpdate(BaseModel):
    date: str | None = None
    content: str | None = None
    mood: str | None = None
    weather: str | None = None
    images: list[str] | None = None


class DiaryResponse(BaseModel):
    id: int
    date: str
    content: str
    mood: str | None = None
    weather: str | None = None
    images: list[str] = []

    model_config = {"from_attributes": True}
