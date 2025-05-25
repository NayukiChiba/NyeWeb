"""
管理员 Pydantic Schemas
"""

from pydantic import BaseModel


class AdminLoginRequest(BaseModel):
    username: str
    password: str


class AdminLoginResponse(BaseModel):
    message: str
    token: str
    username: str
