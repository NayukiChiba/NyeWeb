"""
待办事项 API 路由
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.todo import TodoCreate, TodoUpdate
from app.services import todo as todo_service

router = APIRouter()


@router.get("/todos")
def get_todos(db: Session = Depends(get_db)):
    return todo_service.get_active_todos(db)


@router.get("/admin/todos")
def get_all_todos(db: Session = Depends(get_db)):
    return todo_service.get_all_todos(db)


@router.get("/todos/{todo_id}")
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    return todo_service.get_todo_by_id(db, todo_id)


@router.post("/todos")
def create_todo(data: TodoCreate, db: Session = Depends(get_db)):
    return todo_service.create_todo(
        db,
        data.task,
        data.priority,
        data.type,
        data.progress,
        data.icon,
        data.status,
    )


@router.put("/todos/{todo_id}")
def update_todo(todo_id: int, data: TodoUpdate, db: Session = Depends(get_db)):
    return todo_service.update_todo(
        db,
        todo_id,
        data.task,
        data.completed,
        data.priority,
        data.type,
        data.progress,
        data.icon,
        data.status,
    )


@router.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    return todo_service.delete_todo(db, todo_id)
