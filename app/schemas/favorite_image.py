"""
收藏图片 Pydantic Schemas
"""

from pydantic import BaseModel


class FavoriteImageCreate(BaseModel):
    url: str


class FavoriteImageUpdate(BaseModel):
    url: str


class FavoriteImageResponse(BaseModel):
    id: int
    url: str

    model_config = {"from_attributes": True}
