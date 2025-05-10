"""
待办事项服务层
"""

import logging

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.models import Todo

logger = logging.getLogger("app.services.todo")


def _todo_to_dict(item: Todo) -> dict:
    return {
        "id": item.id,
        "task": item.task,
        "completed": item.completed,
        "priority": item.priority,
        "type": item.type,
        "progress": item.progress,
        "icon": item.icon,
        "status": item.status,
    }


def get_all_todos(db: Session) -> list[dict]:
    items = db.query(Todo).order_by(Todo.id.desc()).all()
    return [_todo_to_dict(t) for t in items]


def get_active_todos(db: Session) -> list[dict]:
    items = (
        db.query(Todo).filter(Todo.status == "active").order_by(Todo.id.desc()).all()
    )
    return [_todo_to_dict(t) for t in items]


def get_todo_by_id(db: Session, todo_id: int) -> dict:
    item = db.query(Todo).filter(Todo.id == todo_id).first()
    if not item:
        raise NotFoundError("待办事项")
    return _todo_to_dict(item)


def create_todo(
    db: Session,
    task: str,
    priority: str = "medium",
    todo_type: str = "short-term",
    progress: int = 0,
    icon: str | None = None,
    status: str = "active",
) -> dict:
    item = Todo(
        task=task,
        priority=priority,
        type=todo_type,
        progress=progress,
        icon=icon,
        status=status,
        completed=(status == "completed"),
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return {"message": "待办创建成功", "id": item.id}


def update_todo(
    db: Session,
    todo_id: int,
    task: str | None = None,
    completed: bool | None = None,
    priority: str | None = None,
    todo_type: str | None = None,
    progress: int | None = None,
    icon: str | None = None,
    status: str | None = None,
) -> dict:
    item = db.query(Todo).filter(Todo.id == todo_id).first()
    if not item:
        raise NotFoundError("待办事项")

    if task is not None:
        item.task = task
    if completed is not None:
        item.completed = completed
        if completed:
            item.status = "completed"
            item.progress = 100
    if priority is not None:
        item.priority = priority
    if todo_type is not None:
        item.type = todo_type
    if progress is not None:
        item.progress = progress
    if icon is not None:
        item.icon = icon
    if status is not None:
        item.status = status
        if status == "completed":
            item.completed = True

    db.commit()
    return {"message": "待办更新成功"}


def delete_todo(db: Session, todo_id: int) -> dict:
    item = db.query(Todo).filter(Todo.id == todo_id).first()
    if not item:
        raise NotFoundError("待办事项")
    db.delete(item)
    db.commit()
    return {"message": "待办删除成功"}
