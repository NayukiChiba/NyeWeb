"""
管理员 API 路由
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.admin import AdminLoginRequest, AdminLoginResponse
from app.services import admin as admin_service

router = APIRouter()


@router.post("/admin/login", response_model=AdminLoginResponse)
def admin_login(data: AdminLoginRequest, db: Session = Depends(get_db)):
    return admin_service.admin_login(db, data.username, data.password)


@router.post("/admin/logout")
def admin_logout(token: str, db: Session = Depends(get_db)):
    return admin_service.admin_logout(db, token)


@router.get("/admin/verify")
def verify_token(token: str, db: Session = Depends(get_db)):
    return admin_service.verify_admin_token(db, token)
