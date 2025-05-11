"""
收藏图片服务层
"""

import logging

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError, BadRequestError
from app.models import FavoriteImage

logger = logging.getLogger("app.services.favorite_image")


def get_all_favorite_images(db: Session) -> list[dict]:
    images = db.query(FavoriteImage).all()
    return [
        {"id": img.id, "url": img.url or "https://ooo.0x0.ooo/2025/09/18/OlGAw6.jpg"}
        for img in images
    ]


def get_favorite_image_by_id(db: Session, image_id: int) -> dict:
    img = db.query(FavoriteImage).filter(FavoriteImage.id == image_id).first()
    if not img:
        raise NotFoundError("收藏图片")
    return {"id": img.id, "url": img.url or "https://ooo.0x0.ooo/2025/09/18/OlGAw6.jpg"}


def create_favorite_image(db: Session, url: str) -> dict:
    count = db.query(FavoriteImage).count()
    if count >= 5:
        raise BadRequestError("收藏图片数量已达到限制（最多5张）")
    img = FavoriteImage(url=url)
    db.add(img)
    db.commit()
    db.refresh(img)
    return {"id": img.id, "url": img.url, "message": "收藏图片创建成功"}


def update_favorite_image(db: Session, image_id: int, url: str) -> dict:
    img = db.query(FavoriteImage).filter(FavoriteImage.id == image_id).first()
    if not img:
        raise NotFoundError("收藏图片")
    img.url = url
    db.commit()
    db.refresh(img)
    return {"id": img.id, "url": img.url, "message": "收藏图片更新成功"}


def delete_favorite_image(db: Session, image_id: int) -> dict:
    img = db.query(FavoriteImage).filter(FavoriteImage.id == image_id).first()
    if not img:
        raise NotFoundError("收藏图片")
    db.delete(img)
    db.commit()
    return {"message": "收藏图片删除成功"}
