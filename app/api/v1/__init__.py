"""
API v1 路由聚合
"""

from fastapi import APIRouter

from app.api.v1 import (
    articles,
    projects,
    books,
    tools,
    timeline,
    favorite_images,
    admin,
    diaries,
    gallery,
    todos,
)

router = APIRouter(prefix="/api")

router.include_router(articles.router, tags=["articles"])
router.include_router(projects.router, tags=["projects"])
router.include_router(books.router, tags=["books"])
router.include_router(tools.router, tags=["tools"])
router.include_router(timeline.router, tags=["timeline"])
router.include_router(favorite_images.router, tags=["favorite-images"])
router.include_router(diaries.router, tags=["diaries"])
router.include_router(gallery.router, tags=["gallery"])
router.include_router(todos.router, tags=["todos"])
router.include_router(admin.router, tags=["admin"])
