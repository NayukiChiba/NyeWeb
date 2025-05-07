"""
书籍服务层 — 链接形式
"""

import logging
import re

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError, BadRequestError
from app.models import Book, BookTag, Tag
from app.schemas.book import BookCreate, BookUpdate
from app.services.tag import (
    sync_tags,
    get_entity_tags,
    get_all_tags_with_counts,
    STATUS_TO_INT,
    INT_TO_STATUS,
)

logger = logging.getLogger("app.services.book")

DEFAULT_COVER = "https://ooo.0x0.ooo/2025/09/18/OlGAw6.jpg"
COVER_URL_PATTERN = re.compile(
    r"^https?://.+\.(jpg|jpeg|png|gif|webp)(\?.*)?$", re.IGNORECASE
)


def _normalize_cover(cover: str | None) -> str:
    if not cover or cover == "/avatar.jpg":
        return DEFAULT_COVER
    if not COVER_URL_PATTERN.match(cover):
        return DEFAULT_COVER
    return cover


def _book_to_dict(db: Session, book: Book, include_status: bool = False) -> dict:
    tags = get_entity_tags(db, book.id, BookTag, "book_id")
    result = {
        "id": book.id,
        "title": book.title,
        "description": book.description,
        "cover": _normalize_cover(book.cover),
        "url": book.url,
        "tags": tags,
    }
    if include_status:
        result["status"] = INT_TO_STATUS.get(book.status, "draft")
    return result


# ── 查询 ──


def get_books_paginated(
    db: Session, page: int, limit: int, search: str | None, tags: str | None
) -> dict:
    query = db.query(Book).filter(Book.status == 1)
    if search:
        like = f"%{search}%"
        query = query.filter((Book.title.ilike(like)) | (Book.description.ilike(like)))
    if tags:
        tag_list = [t.strip() for t in tags.split(",") if t.strip()]
        for tag_name in tag_list:
            subquery = (
                db.query(BookTag.book_id)
                .join(Tag)
                .filter(Tag.name == tag_name)
                .subquery()
            )
            query = query.filter(Book.id.in_(subquery))

    total = query.count()
    offset = (page - 1) * limit
    books = query.offset(offset).limit(limit).all()
    return {
        "data": [_book_to_dict(db, b) for b in books],
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "pages": (total + limit - 1) // limit if limit > 0 else 0,
        },
    }


def get_book_by_id(db: Session, book_id: int) -> dict:
    book = db.query(Book).filter(Book.id == book_id, Book.status == 1).first()
    if not book:
        raise NotFoundError("书籍")
    return _book_to_dict(db, book)


def get_all_books_admin(db: Session) -> list[dict]:
    return [_book_to_dict(db, b, include_status=True) for b in db.query(Book).all()]


def get_all_book_tags(db: Session) -> dict:
    return get_all_tags_with_counts(db, Book, BookTag, "book_id")


# ── 写入 ──


def create_book(db: Session, data: BookCreate) -> dict:
    if not data.url.startswith(("http://", "https://")):
        raise BadRequestError("链接必须以http://或https://开头")

    book = Book(
        title=data.title,
        description=data.description,
        cover=_normalize_cover(data.cover),
        url=data.url,
        status=STATUS_TO_INT.get(data.status, 0),
    )
    db.add(book)
    db.commit()
    db.refresh(book)

    if data.tags:
        sync_tags(db, book.id, data.tags, BookTag, "book_id")
        db.commit()

    return {"message": "图书创建成功", "id": book.id, "url": book.url}


def update_book(db: Session, book_id: int, data: BookUpdate) -> dict:
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise NotFoundError("书籍")
    if data.title is not None:
        book.title = data.title
    if data.description is not None:
        book.description = data.description
    if data.cover is not None:
        book.cover = _normalize_cover(data.cover)
    if data.url is not None:
        book.url = data.url
    if data.status is not None and data.status in STATUS_TO_INT:
        book.status = STATUS_TO_INT[data.status]
    if data.tags is not None:
        sync_tags(db, book.id, data.tags, BookTag, "book_id")
    db.commit()
    return {"message": "图书信息编辑成功", "id": book.id, "title": book.title}


def update_book_status(db: Session, book_id: int, status: str) -> dict:
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise NotFoundError("书籍")
    if status not in STATUS_TO_INT:
        raise BadRequestError("无效的状态值")
    book.status = STATUS_TO_INT[status]
    db.commit()
    return {"message": "书籍状态修改成功", "status": status}


def delete_book(db: Session, book_id: int) -> dict:
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise NotFoundError("书籍")
    db.query(BookTag).filter(BookTag.book_id == book_id).delete()
    db.delete(book)
    db.commit()
    return {"message": "书籍删除成功"}
