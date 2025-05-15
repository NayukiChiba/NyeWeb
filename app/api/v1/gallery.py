"""
图库 API 路由
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.gallery import GalleryCreate, GalleryUpdate
from app.services import gallery as gallery_service

router = APIRouter()


@router.get("/gallery")
def get_gallery(db: Session = Depends(get_db)):
    return gallery_service.get_published_gallery(db)


@router.get("/admin/gallery")
def get_gallery_admin(db: Session = Depends(get_db)):
    return gallery_service.get_all_gallery_admin(db)


@router.get("/gallery/{gallery_id}")
def get_gallery_item(gallery_id: int, db: Session = Depends(get_db)):
    return gallery_service.get_gallery_by_id(db, gallery_id)


@router.post("/gallery")
def create_gallery(data: GalleryCreate, db: Session = Depends(get_db)):
    return gallery_service.create_gallery(
        db,
        data.title,
        data.url,
        data.date,
        data.tags,
        data.status,
    )


@router.put("/gallery/{gallery_id}")
def update_gallery(gallery_id: int, data: GalleryUpdate, db: Session = Depends(get_db)):
    return gallery_service.update_gallery(
        db,
        gallery_id,
        data.title,
        data.url,
        data.date,
        data.tags,
        data.status,
    )


@router.patch("/gallery/{gallery_id}/status")
def update_gallery_status(
    gallery_id: int, status_data: dict, db: Session = Depends(get_db)
):
    return gallery_service.update_gallery(
        db, gallery_id, status=status_data.get("status")
    )


@router.delete("/gallery/{gallery_id}")
def delete_gallery(gallery_id: int, db: Session = Depends(get_db)):
    return gallery_service.delete_gallery(db, gallery_id)
