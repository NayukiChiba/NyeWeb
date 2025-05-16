"""
时间线 API 路由
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.timeline import TimelineCreate
from app.services import timeline as timeline_service

router = APIRouter()


@router.get("/timeline/database")
def get_timeline_from_database(db: Session = Depends(get_db)):
    return timeline_service.get_timeline_database(db)


@router.get("/timeline")
def get_timeline(db: Session = Depends(get_db)):
    return timeline_service.get_timeline(db)


@router.post("/timeline")
def create_timeline_item(data: TimelineCreate, db: Session = Depends(get_db)):
    return timeline_service.create_timeline_item(db, data.timestamp, data.content)


@router.put("/timeline/{item_id}")
def update_timeline_item(
    item_id: int, data: TimelineCreate, db: Session = Depends(get_db)
):
    return timeline_service.update_timeline_item(
        db, item_id, data.timestamp, data.content
    )


@router.delete("/timeline/{item_id}")
def delete_timeline_item(item_id: int, db: Session = Depends(get_db)):
    return timeline_service.delete_timeline_item(db, item_id)
