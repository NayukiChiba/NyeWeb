"""
收藏图片 API 路由
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.favorite_image import FavoriteImageCreate, FavoriteImageUpdate
from app.services import favorite_image as fav_service

router = APIRouter()


@router.get("/favorite-images")
def get_favorite_images(db: Session = Depends(get_db)):
    return fav_service.get_all_favorite_images(db)


@router.get("/favorite-images/{image_id}")
def get_favorite_image_by_id(image_id: int, db: Session = Depends(get_db)):
    return fav_service.get_favorite_image_by_id(db, image_id)


@router.post("/favorite-images")
def create_favorite_image(data: FavoriteImageCreate, db: Session = Depends(get_db)):
    return fav_service.create_favorite_image(db, data.url)


@router.put("/favorite-images/{image_id}")
def update_favorite_image(
    image_id: int, data: FavoriteImageUpdate, db: Session = Depends(get_db)
):
    return fav_service.update_favorite_image(db, image_id, data.url)


@router.delete("/favorite-images/{image_id}")
def delete_favorite_image(image_id: int, db: Session = Depends(get_db)):
    return fav_service.delete_favorite_image(db, image_id)
