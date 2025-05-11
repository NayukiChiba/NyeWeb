"""
时间线服务层
"""

import logging
from datetime import datetime

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError, BadRequestError
from app.models import Timeline

logger = logging.getLogger("app.services.timeline")


def _timeline_to_dict(item: Timeline) -> dict:
    return {
        "id": item.id,
        "timestamp": item.timestamp.isoformat() if item.timestamp else None,
        "content": item.content,
    }


def get_timeline(db: Session) -> list[dict]:
    items = db.query(Timeline).order_by(Timeline.timestamp.desc()).all()
    return [_timeline_to_dict(i) for i in items]


def get_timeline_database(db: Session) -> dict:
    """兼容旧的 /timeline/database 端点返回格式"""
    items = db.query(Timeline).order_by(Timeline.timestamp.desc()).all()
    data = [_timeline_to_dict(i) for i in items]
    return {
        "status": "success",
        "data": data,
        "total": len(data),
        "message": f"成功获取 {len(data)} 条时间线数据",
    }


def create_timeline_item(db: Session, timestamp_str: str, content: str) -> dict:
    try:
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        raise BadRequestError("时间格式错误，请使用 YYYY-MM-DD HH:MM:SS 格式")

    item = Timeline(timestamp=timestamp, content=content)
    db.add(item)
    db.commit()
    db.refresh(item)
    return {"message": "时间线项目创建成功", "id": item.id}


def update_timeline_item(
    db: Session, item_id: int, timestamp_str: str, content: str
) -> dict:
    item = db.query(Timeline).filter(Timeline.id == item_id).first()
    if not item:
        raise NotFoundError("时间线项目")
    try:
        item.timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        raise BadRequestError("时间格式错误，请使用 YYYY-MM-DD HH:MM:SS 格式")
    item.content = content
    db.commit()
    return {"message": "时间线项目更新成功"}


def delete_timeline_item(db: Session, item_id: int) -> dict:
    item = db.query(Timeline).filter(Timeline.id == item_id).first()
    if not item:
        raise NotFoundError("时间线项目")
    db.delete(item)
    db.commit()
    return {"message": "时间线项目删除成功"}
