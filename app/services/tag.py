"""
通用标签服务 — 消除各模块重复的标签 CRUD 代码
"""

import logging

from sqlalchemy.orm import Session

from app.models.tag import Tag

logger = logging.getLogger("app.services.tag")

# 状态映射（通用）
STATUS_TO_INT = {"draft": 0, "published": 1, "recycled": 2}
INT_TO_STATUS = {0: "draft", 1: "published", 2: "recycled"}


def get_or_create_tag(db: Session, tag_name: str) -> Tag:
    """获取或创建标签"""
    tag_name = tag_name.strip()
    tag = db.query(Tag).filter(Tag.name == tag_name).first()
    if not tag:
        tag = Tag(name=tag_name)
        db.add(tag)
        db.flush()
        logger.info("创建新标签: %s", tag_name)
    return tag


def sync_tags(
    db: Session,
    entity_id: int,
    tag_names: list[str],
    assoc_model,
    id_column_name: str,
) -> None:
    """
    同步实体的标签关联。
    1. 删除旧关联
    2. 创建新关联

    Args:
        db: 数据库 Session
        entity_id: 实体 ID
        tag_names: 新的标签名列表
        assoc_model: 关联表模型 (如 ArticleTag)
        id_column_name: 关联表中的实体 ID 列名 (如 "article_id")
    """
    # 删除旧标签关联
    db.query(assoc_model).filter(
        getattr(assoc_model, id_column_name) == entity_id
    ).delete()

    # 创建新标签关联
    for name in tag_names:
        if not name.strip():
            continue
        tag = get_or_create_tag(db, name)
        assoc = assoc_model(**{id_column_name: entity_id, "tag_id": tag.id})
        db.add(assoc)


def get_entity_tags(
    db: Session, entity_id: int, assoc_model, id_column_name: str
) -> list[str]:
    """获取实体关联的所有标签名"""
    tags = (
        db.query(Tag)
        .join(assoc_model)
        .filter(getattr(assoc_model, id_column_name) == entity_id)
        .all()
    )
    return [tag.name for tag in tags]


def get_all_tags_with_counts(
    db: Session,
    entity_model,
    assoc_model,
    id_column_name: str,
    published_only: bool = True,
) -> dict:
    """获取所有标签及其关联数量"""
    query = db.query(entity_model)
    if published_only and hasattr(entity_model, "status"):
        query = query.filter(entity_model.status == 1)

    entities = query.all()
    all_tags = []
    tag_counts = {}

    for entity in entities:
        tags = get_entity_tags(db, entity.id, assoc_model, id_column_name)
        for tag_name in tags:
            if tag_name not in all_tags:
                all_tags.append(tag_name)
            tag_counts[tag_name] = tag_counts.get(tag_name, 0) + 1

    return {"tags": all_tags, "counts": tag_counts}
