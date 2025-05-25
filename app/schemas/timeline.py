"""
时间线 Pydantic Schemas
"""

from typing import Optional

from pydantic import BaseModel


class TimelineCreate(BaseModel):
    timestamp: str
    content: str


class TimelineUpdate(BaseModel):
    timestamp: Optional[str] = None
    content: Optional[str] = None


class TimelineResponse(BaseModel):
    id: int
    timestamp: Optional[str] = None
    content: str

    model_config = {"from_attributes": True}
