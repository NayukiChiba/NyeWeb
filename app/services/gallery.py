"""
图库服务层
"""

import logging
from datetime import datetime

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError, BadRequestError
from app.models import Gallery
from app.services.tag import STATUS_TO_INT, INT_TO_STATUS

logger = logging.getLogger("app.services.gallery")


def _gallery_to_dict(item: Gallery, include_status: bool = False) -> dict:
    result = {
        "id": item.id,
        "title": item.title,
        "url": item.url,
        "date": item.date.strftime("%Y-%m-%d") if item.date else None,
        "tags": item.tags or [],
    }
    if include_status:
        result["status"] = INT_TO_STATUS.get(item.status, "draft")
    return result


def get_published_gallery(db: Session) -> list[dict]:
    items = (
        db.query(Gallery).filter(Gallery.status == 1).order_by(Gallery.id.desc()).all()
    )
    return [_gallery_to_dict(g) for g in items]


def get_all_gallery_admin(db: Session) -> list[dict]:
    items = db.query(Gallery).order_by(Gallery.id.desc()).all()
    return [_gallery_to_dict(g, include_status=True) for g in items]


def get_gallery_by_id(db: Session, gallery_id: int) -> dict:
    item = db.query(Gallery).filter(Gallery.id == gallery_id).first()
    if not item:
        raise NotFoundError("图片")
    return _gallery_to_dict(item, include_status=True)


def create_gallery(
    db: Session,
    title: str,
    url: str,
    date_str: str | None = None,
    tags: list[str] | None = None,
    status: str = "published",
) -> dict:
    gallery_date = None
    if date_str:
        try:
            gallery_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            raise BadRequestError("日期格式错误，请使用 YYYY-MM-DD 格式")

    item = Gallery(
        title=title,
        url=url,
        date=gallery_date,
        tags=tags or [],
        status=STATUS_TO_INT.get(status, 1),
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return {"message": "图片添加成功", "id": item.id}


def update_gallery(
    db: Session,
    gallery_id: int,
    title: str | None = None,
    url: str | None = None,
    date_str: str | None = None,
    tags: list[str] | None = None,
    status: str | None = None,
) -> dict:
    item = db.query(Gallery).filter(Gallery.id == gallery_id).first()
    if not item:
        raise NotFoundError("图片")

    if title is not None:
        item.title = title
    if url is not None:
        item.url = url
    if date_str is not None:
        try:
            item.date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            raise BadRequestError("日期格式错误")
    if tags is not None:
        item.tags = tags
    if status is not None and status in STATUS_TO_INT:
        item.status = STATUS_TO_INT[status]

    db.commit()
    return {"message": "图片更新成功"}


def delete_gallery(db: Session, gallery_id: int) -> dict:
    item = db.query(Gallery).filter(Gallery.id == gallery_id).first()
    if not item:
        raise NotFoundError("图片")
    db.delete(item)
    db.commit()
    return {"message": "图片删除成功"}
