"""
日记服务层
"""

import logging
from datetime import datetime

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError, BadRequestError
from app.models import Diary

logger = logging.getLogger("app.services.diary")


def _diary_to_dict(diary: Diary) -> dict:
    return {
        "id": diary.id,
        "date": diary.date.strftime("%Y-%m-%dT%H:%M") if diary.date else None,
        "content": diary.content,
        "mood": diary.mood,
        "weather": diary.weather,
        "images": diary.images or [],
    }


def get_all_diaries(db: Session) -> list[dict]:
    items = db.query(Diary).order_by(Diary.date.desc()).all()
    return [_diary_to_dict(d) for d in items]


def get_diary_by_id(db: Session, diary_id: int) -> dict:
    diary = db.query(Diary).filter(Diary.id == diary_id).first()
    if not diary:
        raise NotFoundError("日记")
    return _diary_to_dict(diary)


def create_diary(
    db: Session,
    date_str: str,
    content: str,
    mood: str | None = None,
    weather: str | None = None,
    images: list[str] | None = None,
) -> dict:
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M")
    except ValueError:
        raise BadRequestError("日期格式错误，请使用 YYYY-MM-DDTHH:MM 格式")

    diary = Diary(
        date=dt, content=content, mood=mood, weather=weather, images=images or []
    )
    db.add(diary)
    db.commit()
    db.refresh(diary)
    return {"message": "日记创建成功", "id": diary.id}


def update_diary(
    db: Session,
    diary_id: int,
    date_str: str | None = None,
    content: str | None = None,
    mood: str | None = None,
    weather: str | None = None,
    images: list[str] | None = None,
) -> dict:
    diary = db.query(Diary).filter(Diary.id == diary_id).first()
    if not diary:
        raise NotFoundError("日记")

    if date_str is not None:
        try:
            diary.date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M")
        except ValueError:
            raise BadRequestError("日期格式错误")
    if content is not None:
        diary.content = content
    if mood is not None:
        diary.mood = mood
    if weather is not None:
        diary.weather = weather
    if images is not None:
        diary.images = images

    db.commit()
    return {"message": "日记更新成功"}


def delete_diary(db: Session, diary_id: int) -> dict:
    diary = db.query(Diary).filter(Diary.id == diary_id).first()
    if not diary:
        raise NotFoundError("日记")
    db.delete(diary)
    db.commit()
    return {"message": "日记删除成功"}
