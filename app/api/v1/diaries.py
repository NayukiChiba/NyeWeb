"""
日记 API 路由
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.diary import DiaryCreate, DiaryUpdate
from app.services import diary as diary_service

router = APIRouter()


@router.get("/diaries")
def get_diaries(db: Session = Depends(get_db)):
    return diary_service.get_all_diaries(db)


@router.get("/diaries/{diary_id}")
def get_diary(diary_id: int, db: Session = Depends(get_db)):
    return diary_service.get_diary_by_id(db, diary_id)


@router.post("/diaries")
def create_diary(data: DiaryCreate, db: Session = Depends(get_db)):
    return diary_service.create_diary(
        db,
        data.date,
        data.content,
        data.mood,
        data.weather,
        data.images,
    )


@router.put("/diaries/{diary_id}")
def update_diary(diary_id: int, data: DiaryUpdate, db: Session = Depends(get_db)):
    return diary_service.update_diary(
        db,
        diary_id,
        data.date,
        data.content,
        data.mood,
        data.weather,
        data.images,
    )


@router.delete("/diaries/{diary_id}")
def delete_diary(diary_id: int, db: Session = Depends(get_db)):
    return diary_service.delete_diary(db, diary_id)
