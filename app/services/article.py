"""
文章服务层 — 使用 content/blog/ 目录管理文章内容
"""

import logging
import os
import re
from datetime import datetime

from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.exceptions import NotFoundError, BadRequestError
from app.models import Article, ArticleTag
from app.schemas.article import ArticleCreate, ArticleUpdate
from app.services.tag import (
    sync_tags,
    get_entity_tags,
    get_all_tags_with_counts,
    STATUS_TO_INT,
    INT_TO_STATUS,
)

logger = logging.getLogger("app.services.article")
settings = get_settings()


def _count_words(text: str) -> int:
    """统计中英文混合字数"""
    text = re.sub(r"[#*`>\[\]\(\)\-_|!]", "", text)  # 去除 Markdown 符号
    chinese = re.findall(r"[\u4e00-\u9fa5]", text)
    english = re.findall(r"[a-zA-Z]+", text)
    return len(chinese) + len(english)


def _article_to_dict(
    db: Session, article: Article, include_status: bool = False
) -> dict:
    """将 Article ORM 对象转为前端格式 dict"""
    tags = get_entity_tags(db, article.id, ArticleTag, "article_id")
    result = {
        "id": article.id,
        "title": article.title,
        "slug": article.slug,
        "description": article.description,
        "category": article.category,
        "image": article.image,
        "date": article.date.strftime("%Y-%m-%d") if article.date else None,
        "word_count": article.word_count or 0,
        "tags": tags,
    }
    if include_status:
        result["status"] = INT_TO_STATUS.get(article.status, "draft")
        result["updated_at"] = (
            article.updated_at.strftime("%Y-%m-%d %H:%M:%S")
            if article.updated_at
            else None
        )
    return result


def generate_safe_slug(text: str) -> str:
    """生成安全的 slug"""
    if not text:
        return "untitled"
    slug = text.lower().strip()
    slug = re.sub(r"[^\w\u4e00-\u9fa5]+", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    slug = slug.strip("-")
    return slug or "untitled"


def _get_content_path(category: str | None = None) -> str:
    """获取文章内容目录路径"""
    base = settings.content_dir
    if category:
        return os.path.join(base, category.replace("/", os.sep))
    return base


def _get_article_file_path(slug: str, category: str | None = None) -> str:
    """获取文章 Markdown 文件路径"""
    return os.path.join(_get_content_path(category), f"{slug}.md")


def _read_article_content(slug: str, category: str | None = None) -> str | None:
    """从 content/blog/ 读取文章内容"""
    file_path = _get_article_file_path(slug, category)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    return None


# ── 查询 ──────────────────────────────────────────────────


def get_published_articles(db: Session) -> list[dict]:
    """获取所有已发布文章"""
    articles = (
        db.query(Article)
        .filter(Article.status == 1)
        .order_by(Article.date.desc())
        .all()
    )
    return [_article_to_dict(db, a) for a in articles]


def get_all_articles_admin(db: Session) -> list[dict]:
    """管理员获取所有文章（所有状态）"""
    articles = db.query(Article).order_by(Article.date.desc()).all()
    return [_article_to_dict(db, a, include_status=True) for a in articles]


def get_article_by_slug(db: Session, slug: str) -> dict:
    """根据 slug 获取已发布文章 + 内容"""
    article = (
        db.query(Article).filter(Article.slug == slug, Article.status == 1).first()
    )
    if not article:
        raise NotFoundError("文章")
    result = _article_to_dict(db, article)
    result["content"] = _read_article_content(slug, article.category)
    return result


def get_article_by_category_and_slug(db: Session, category: str, slug: str) -> dict:
    """根据分类和 slug 获取已发布文章 + 内容"""
    article = (
        db.query(Article)
        .filter(Article.category == category, Article.slug == slug, Article.status == 1)
        .first()
    )
    if not article:
        raise NotFoundError("文章")
    result = _article_to_dict(db, article)
    result["content"] = _read_article_content(slug, category)
    return result


# ── 分类 ──────────────────────────────────────────────────


def scan_physical_categories(db: Session) -> dict:
    """扫描 content/blog/ 目录获取分类树"""
    base_path = settings.content_dir
    os.makedirs(base_path, exist_ok=True)

    categories = []
    abs_base_path = os.path.abspath(base_path)

    if not os.path.exists(abs_base_path):
        return {"categories": [], "total": 0}

    for root, dirs, files in os.walk(abs_base_path):
        # 跳过 Obsidian 和隐藏目录
        dirs[:] = [
            d
            for d in dirs
            if not d.startswith(".")
            and d not in ("__pycache__", "assets", "_templates", "_copilot")
        ]
        rel_path = os.path.relpath(root, abs_base_path)
        if rel_path == ".":
            continue

        category_path = rel_path.replace(os.sep, "/")
        path_parts = category_path.split("/")
        if any(part.startswith(".") or part.startswith("_") for part in path_parts):
            continue

        md_files = [
            f
            for f in files
            if f.endswith(".md")
            and f not in ("README.md", ".gitkeep", "index.md")
            and not f.startswith(".")
        ]

        articles_info = []
        for md_file in md_files:
            article_slug = md_file[:-3]
            article = (
                db.query(Article)
                .filter(
                    Article.slug == article_slug,
                    Article.category == category_path,
                    Article.status == 1,
                )
                .first()
            )
            if article:
                articles_info.append(
                    {
                        "slug": article.slug,
                        "title": article.title,
                        "description": article.description,
                        "date": article.date.strftime("%Y-%m-%d")
                        if article.date
                        else None,
                    }
                )
            else:
                articles_info.append(
                    {
                        "slug": article_slug,
                        "title": article_slug.replace("-", " ").title(),
                        "description": None,
                        "date": None,
                    }
                )

        categories.append(
            {"path": category_path, "count": len(md_files), "articles": articles_info}
        )

    return {"categories": categories, "total": len(categories)}


def create_category_folder(name: str, path: str | None, parent: str | None) -> dict:
    """在 content/blog/ 中创建分类文件夹"""
    if not path:
        safe_name = name.strip()
        safe_name = re.sub(r"[^\w\u4e00-\u9fa5\-]", "-", safe_name)
        safe_name = re.sub(r"-+", "-", safe_name).strip("-")
        path = f"{parent}/{safe_name}" if parent else safe_name

    if not path:
        raise BadRequestError("分类路径不能为空")

    full_path = os.path.join(settings.content_dir, path.replace("/", os.sep))
    if os.path.exists(full_path):
        from app.core.exceptions import ConflictError

        raise ConflictError("分类文件夹已存在")
    os.makedirs(full_path, exist_ok=True)

    return {"message": "分类文件夹创建成功", "name": name, "path": path}


# ── 写入 ──────────────────────────────────────────────────


def _save_article_file(
    article: Article, content: str, category: str | None = None
) -> None:
    """保存文章 Markdown 文件到 content/blog/"""
    dir_path = _get_content_path(category)
    os.makedirs(dir_path, exist_ok=True)

    file_content = content
    if not content.strip().startswith("#"):
        file_content = f"# {article.title}\n\n{content}"

    file_path = os.path.join(dir_path, f"{article.slug}.md")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(file_content)
    logger.info("保存文章文件: %s", file_path)


def create_article(db: Session, data: ArticleCreate) -> dict:
    """创建新文章"""
    slug = generate_safe_slug(data.slug or data.title)
    base_slug = slug
    counter = 1
    while db.query(Article).filter(Article.slug == slug).first():
        slug = f"{base_slug}-{counter}"
        counter += 1

    article_date = datetime.now().date()
    if data.date:
        try:
            article_date = datetime.strptime(data.date, "%Y-%m-%d").date()
        except ValueError:
            logger.warning("日期格式错误，使用当前日期: %s", data.date)

    status = STATUS_TO_INT.get(data.status, 0)
    word_count = _count_words(data.content) if data.content else 0

    article = Article(
        title=data.title,
        slug=slug,
        description=data.description,
        category=data.category,
        date=article_date,
        status=status,
        image=data.image,
        word_count=word_count,
        updated_at=datetime.now(),
    )
    db.add(article)
    db.commit()
    db.refresh(article)

    if data.tags:
        sync_tags(db, article.id, data.tags, ArticleTag, "article_id")
        db.commit()

    try:
        _save_article_file(article, data.content, data.category)
    except Exception as e:
        logger.warning("保存文章文件失败: %s", e)

    return {"message": "文章上传成功", "id": article.id, "slug": article.slug}


def update_article(db: Session, article_id: int, data: ArticleUpdate) -> dict:
    """更新文章"""
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise NotFoundError("文章")

    if data.title is not None:
        article.title = data.title
    if data.category is not None:
        article.category = data.category
    if data.description is not None:
        article.description = data.description
    if data.image is not None:
        article.image = data.image
    if data.date is not None:
        try:
            article.date = datetime.strptime(data.date, "%Y-%m-%d").date()
        except ValueError:
            pass
    if data.status is not None and data.status in STATUS_TO_INT:
        article.status = STATUS_TO_INT[data.status]
    if data.tags is not None:
        sync_tags(db, article.id, data.tags, ArticleTag, "article_id")
    if data.content is not None:
        article.word_count = _count_words(data.content)
        try:
            _save_article_file(article, data.content, article.category)
        except Exception as e:
            logger.warning("更新文章文件失败: %s", e)

    article.updated_at = datetime.now()
    db.commit()
    return {"message": "文章信息编辑成功", "id": article.id, "title": article.title}


def update_article_status(db: Session, article_id: int, status: str) -> dict:
    """修改文章状态"""
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise NotFoundError("文章")
    if status not in STATUS_TO_INT:
        raise BadRequestError("无效的状态值")
    article.status = STATUS_TO_INT[status]
    db.commit()
    return {"message": "文章状态修改成功", "status": status}


def delete_article(db: Session, article_id: int) -> dict:
    """删除文章"""
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise NotFoundError("文章")

    db.query(ArticleTag).filter(ArticleTag.article_id == article_id).delete()

    # 删除 content/blog/ 中的文件
    file_path = _get_article_file_path(article.slug, article.category)
    if os.path.exists(file_path):
        os.remove(file_path)

    db.delete(article)
    db.commit()
    return {"message": "文章删除成功"}


def get_all_article_tags(db: Session) -> dict:
    """获取所有文章标签"""
    return get_all_tags_with_counts(
        db, Article, ArticleTag, "article_id", published_only=False
    )
