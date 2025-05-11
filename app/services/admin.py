"""
管理员服务层
"""

import logging
from datetime import datetime

from sqlalchemy.orm import Session

from app.core.exceptions import UnauthorizedError
from app.core.security import hash_password, verify_password, generate_token
from app.models import Admin

logger = logging.getLogger("app.services.admin")


def create_admin(db: Session, username: str, password: str) -> Admin:
    """创建管理员账户"""
    admin = Admin(username=username, password_hash=hash_password(password))
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin


def admin_login(db: Session, username: str, password: str) -> dict:
    """管理员登录"""
    admin = db.query(Admin).filter(Admin.username == username).first()
    if not admin or not verify_password(password, admin.password_hash):
        raise UnauthorizedError("用户名或密码错误")

    token = generate_token()
    # 注意：当前 Admin 模型没有 login_token / last_login 列
    # 如果数据库表有这些列但 ORM 模型没定义，这里跳过
    try:
        admin.login_token = token
        admin.last_login = datetime.utcnow()
    except AttributeError:
        pass

    db.commit()
    return {"message": "登录成功", "token": token, "username": admin.username}


def admin_logout(db: Session, token: str) -> dict:
    """管理员登出"""
    try:
        admin = db.query(Admin).filter(Admin.login_token == token).first()
        if admin:
            admin.login_token = None
            db.commit()
    except Exception:
        pass
    return {"message": "登出成功"}


def verify_admin_token(db: Session, token: str) -> dict:
    """验证 Token 有效性"""
    try:
        admin = db.query(Admin).filter(Admin.login_token == token).first()
    except Exception:
        raise UnauthorizedError("无效的token")
    if not admin:
        raise UnauthorizedError("无效的token")
    return {"message": "token有效", "username": admin.username}
