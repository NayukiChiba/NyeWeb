"""
书籍 API 路由
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.book import BookCreate, BookUpdate
from app.services import book as book_service

router = APIRouter()


@router.get("/books")
def get_books(
    page: int = 1,
    limit: int = 6,
    search: str = None,
    tags: str = None,
    db: Session = Depends(get_db),
):
    return book_service.get_books_paginated(db, page, limit, search, tags)


@router.get("/book-tags")
def get_all_book_tags(db: Session = Depends(get_db)):
    return book_service.get_all_book_tags(db)


@router.get("/admin/books")
def get_all_books_admin(db: Session = Depends(get_db)):
    return book_service.get_all_books_admin(db)


@router.get("/books/{book_id}")
def get_book_by_id(book_id: int, db: Session = Depends(get_db)):
    return book_service.get_book_by_id(db, book_id)


@router.post("/admin/books")
def create_book(data: BookCreate, db: Session = Depends(get_db)):
    return book_service.create_book(db, data)


@router.put("/admin/books/{book_id}")
def update_book(book_id: int, data: BookUpdate, db: Session = Depends(get_db)):
    return book_service.update_book(db, book_id, data)


@router.patch("/books/{book_id}/status")
def update_book_status(book_id: int, status_data: dict, db: Session = Depends(get_db)):
    return book_service.update_book_status(db, book_id, status_data.get("status"))


@router.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    return book_service.delete_book(db, book_id)
