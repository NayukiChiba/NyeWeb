"""
项目 API 路由 — 链接形式
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.services import project as project_service

router = APIRouter()


@router.get("/projects")
def get_projects(db: Session = Depends(get_db)):
    return project_service.get_published_projects(db)


@router.get("/admin/projects")
def get_all_projects_admin(db: Session = Depends(get_db)):
    return project_service.get_all_projects_admin(db)


@router.get("/project-tags")
def get_all_project_tags(db: Session = Depends(get_db)):
    return project_service.get_all_project_tags(db)


@router.get("/projects/{project_id}")
def get_project_by_id(project_id: int, db: Session = Depends(get_db)):
    return project_service.get_project_by_id(db, project_id)


@router.post("/projects")
def create_project(data: ProjectCreate, db: Session = Depends(get_db)):
    return project_service.create_project(db, data)


@router.put("/projects/{project_id}")
def update_project(project_id: int, data: ProjectUpdate, db: Session = Depends(get_db)):
    return project_service.update_project(db, project_id, data)


@router.patch("/projects/{project_id}/status")
def update_project_status(
    project_id: int, status_data: dict, db: Session = Depends(get_db)
):
    return project_service.update_project_status(
        db, project_id, status_data.get("status")
    )


@router.delete("/projects/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    return project_service.delete_project(db, project_id)
