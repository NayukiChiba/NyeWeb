"""
文章 API 路由
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.article import ArticleCreate, ArticleUpdate, CategoryCreate
from app.services import article as article_service

router = APIRouter()


@router.get("/articles/categories")
def get_article_categories(db: Session = Depends(get_db)):
    return article_service.scan_physical_categories(db)


@router.post("/articles/categories")
def create_category(request: CategoryCreate, db: Session = Depends(get_db)):
    return article_service.create_category_folder(
        request.name, request.path, request.parent
    )


@router.get("/articles")
def get_articles(db: Session = Depends(get_db)):
    return article_service.get_published_articles(db)


@router.get("/admin/articles")
def get_all_articles_admin(db: Session = Depends(get_db)):
    return article_service.get_all_articles_admin(db)


@router.get("/articles/{category:path}/{article_slug}")
def get_article_by_category_and_slug(
    category: str, article_slug: str, db: Session = Depends(get_db)
):
    return article_service.get_article_by_category_and_slug(db, category, article_slug)


@router.get("/articles/{article_slug}")
def get_article_by_slug(article_slug: str, db: Session = Depends(get_db)):
    return article_service.get_article_by_slug(db, article_slug)


@router.post("/articles")
def create_article(data: ArticleCreate, db: Session = Depends(get_db)):
    return article_service.create_article(db, data)


@router.put("/articles/{article_id}")
def update_article(article_id: int, data: ArticleUpdate, db: Session = Depends(get_db)):
    return article_service.update_article(db, article_id, data)


@router.post("/articles/{article_id}/edit")
def update_article_post(
    article_id: int, data: ArticleUpdate, db: Session = Depends(get_db)
):
    return article_service.update_article(db, article_id, data)


@router.patch("/articles/{article_id}/status")
def update_article_status(
    article_id: int, status_data: dict, db: Session = Depends(get_db)
):
    return article_service.update_article_status(
        db, article_id, status_data.get("status")
    )


@router.delete("/articles/{article_id}")
def delete_article(article_id: int, db: Session = Depends(get_db)):
    return article_service.delete_article(db, article_id)


@router.get("/tags")
def get_all_tags(db: Session = Depends(get_db)):
    return article_service.get_all_article_tags(db)
