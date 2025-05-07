"""
项目服务层 — 链接形式，JSON 技术栈
"""

import logging

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError, BadRequestError
from app.models import Project, ProjectTag
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.services.tag import (
    sync_tags,
    get_entity_tags,
    get_all_tags_with_counts,
)

logger = logging.getLogger("app.services.project")

VISIBILITY_MAP = {"draft": 0, "published": 1}
VISIBILITY_REVERSE = {0: "draft", 1: "published"}


def _project_to_dict(
    db: Session, project: Project, include_admin: bool = False
) -> dict:
    tags = get_entity_tags(db, project.id, ProjectTag, "project_id")
    result = {
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "link": project.link,
        "techStack": project.tech_stack or [],
        "status": project.status,
        "tags": tags,
    }
    if include_admin:
        result["visibility"] = VISIBILITY_REVERSE.get(project.visibility, "draft")
    return result


# ── 查询 ──


def get_published_projects(db: Session) -> list[dict]:
    projects = db.query(Project).filter(Project.visibility == 1).all()
    return [_project_to_dict(db, p) for p in projects]


def get_all_projects_admin(db: Session) -> list[dict]:
    projects = db.query(Project).all()
    return [_project_to_dict(db, p, include_admin=True) for p in projects]


def get_project_by_id(db: Session, project_id: int) -> dict:
    project = (
        db.query(Project)
        .filter(Project.id == project_id, Project.visibility == 1)
        .first()
    )
    if not project:
        raise NotFoundError("项目")
    return _project_to_dict(db, project)


def get_all_project_tags(db: Session) -> dict:
    return get_all_tags_with_counts(db, Project, ProjectTag, "project_id")


# ── 写入 ──


def create_project(db: Session, data: ProjectCreate) -> dict:
    if not data.link.startswith(("http://", "https://")):
        raise BadRequestError("项目链接必须以http://或https://开头")

    project = Project(
        name=data.name,
        link=data.link,
        description=data.description,
        tech_stack=data.tech_stack or [],
        status=data.status,
        visibility=VISIBILITY_MAP.get(data.visibility, 0),
    )
    db.add(project)
    db.commit()
    db.refresh(project)

    if data.tech_stack:
        sync_tags(db, project.id, data.tech_stack, ProjectTag, "project_id")
        db.commit()

    return {"message": "项目创建成功", "id": project.id}


def update_project(db: Session, project_id: int, data: ProjectUpdate) -> dict:
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise NotFoundError("项目")

    if data.name is not None:
        project.name = data.name
    if data.link is not None:
        project.link = data.link
    if data.description is not None:
        project.description = data.description
    if data.tech_stack is not None:
        project.tech_stack = data.tech_stack
        sync_tags(db, project.id, data.tech_stack, ProjectTag, "project_id")
    if data.status is not None:
        project.status = data.status
    if data.visibility is not None and data.visibility in VISIBILITY_MAP:
        project.visibility = VISIBILITY_MAP[data.visibility]

    db.commit()
    return {"message": "项目信息编辑成功", "id": project.id, "name": project.name}


def update_project_status(db: Session, project_id: int, status: str) -> dict:
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise NotFoundError("项目")
    project.status = status
    db.commit()
    return {"message": "项目状态修改成功", "status": status}


def delete_project(db: Session, project_id: int) -> dict:
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise NotFoundError("项目")
    db.query(ProjectTag).filter(ProjectTag.project_id == project_id).delete()
    db.delete(project)
    db.commit()
    return {"message": "项目删除成功"}
