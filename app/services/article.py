"""
文章服务层 — 以 content/blog/ 目录为核心，自动扫描 frontmatter
"""

import logging
import os
import re
from datetime import datetime

import yaml
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


# ── 工具函数 ─────────────────────────────────────────────


def _count_words(text: str) -> int:
    """统计中英文混合字数"""
    text = re.sub(r"[#*`>\[\]\(\)\-_|!]", "", text)
    chinese = re.findall(r"[\u4e00-\u9fa5]", text)
    english = re.findall(r"[a-zA-Z]+", text)
    return len(chinese) + len(english)


def _parse_frontmatter(content: str) -> tuple[dict, str]:
    """
    解析 Markdown 文件的 YAML frontmatter。
    返回 (frontmatter_dict, body_content)
    """
    if not content.startswith("---"):
        return {}, content

    # 找到第二个 ---
    end_idx = content.find("---", 3)
    if end_idx == -1:
        return {}, content

    yaml_str = content[3:end_idx].strip()
    body = content[end_idx + 3:].strip()

    try:
        fm = yaml.safe_load(yaml_str)
        if not isinstance(fm, dict):
            fm = {}
    except yaml.YAMLError as e:
        logger.warning("YAML 解析失败: %s", e)
        fm = {}

    return fm, body


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


# ── content 目录读取 ──────────────────────────────────────


def _get_content_file_path(slug: str) -> str:
    """根据 slug（相对路径）获取文章 Markdown 文件绝对路径"""
    return os.path.join(settings.content_dir, f"{slug}.md")


def _read_article_content(slug: str) -> str | None:
    """从 content/blog/ 读取文章内容"""
    file_path = _get_content_file_path(slug)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    logger.warning("未找到文章内容文件: %s", file_path)
    return None


# ── 同步 content → DB ────────────────────────────────────


def sync_articles_from_content(db: Session) -> dict:
    """
    扫描 content/blog/ 所有 .md 文件，解析 frontmatter，
    自动创建或更新数据库中的文章记录。

    slug = 文件相对路径（不含 .md），如 Knowledge/GitUsage
    """
    base = settings.content_dir
    if not os.path.exists(base):
        logger.warning("content 目录不存在: %s", base)
        return {"synced": 0, "created": 0, "updated": 0, "skipped": 0}

    created = 0
    updated = 0
    skipped = 0
    synced_slugs = []

    for root, dirs, files in os.walk(base):
        # 跳过隐藏目录和特殊目录
        dirs[:] = [
            d for d in dirs
            if not d.startswith(".")
            and d not in ("__pycache__", "assets", "_templates", "_copilot")
        ]

        for filename in files:
            if not filename.endswith(".md"):
                continue
            if filename in ("README.md", "index.md", ".gitkeep"):
                continue
            if filename.startswith("."):
                continue

            file_path = os.path.join(root, filename)
            rel_path = os.path.relpath(file_path, base)
            # slug = 相对路径，去掉 .md，使用 / 分隔
            slug = rel_path.replace(os.sep, "/")[:-3]

            # 读取文件内容
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    raw_content = f.read()
            except Exception as e:
                logger.warning("读取文件失败: %s - %s", file_path, e)
                skipped += 1
                continue

            # 解析 frontmatter
            fm, body = _parse_frontmatter(raw_content)

            title = fm.get("title", filename[:-3])
            date_str = fm.get("date")
            category = fm.get("category", "")
            description = fm.get("description", "")
            image = fm.get("image", "")
            status_str = fm.get("status", "published")
            tags = fm.get("tags", [])
            if isinstance(tags, str):
                tags = [t.strip() for t in tags.split(",")]

            # 解析日期
            article_date = None
            if date_str:
                if isinstance(date_str, datetime):
                    article_date = date_str.date()
                elif isinstance(date_str, str):
                    try:
                        article_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                    except ValueError:
                        pass
                else:
                    # date_str might be a date object
                    article_date = date_str

            status = STATUS_TO_INT.get(status_str, 1)
            word_count = _count_words(body)

            # 查找或创建 DB 记录
            article = db.query(Article).filter(Article.slug == slug).first()

            if article:
                # 更新已有记录
                article.title = title
                article.category = category
                article.description = description
                article.image = image
                article.word_count = word_count
                article.status = status
                if article_date:
                    article.date = article_date
                article.updated_at = datetime.now()
                updated += 1
            else:
                # 创建新记录
                article = Article(
                    title=title,
                    slug=slug,
                    category=category,
                    description=description,
                    image=image,
                    date=article_date or datetime.now().date(),
                    word_count=word_count,
                    status=status,
                    updated_at=datetime.now(),
                )
                db.add(article)
                db.flush()  # 获取 ID
                created += 1

            # 同步标签
            if tags:
                sync_tags(db, article.id, tags, ArticleTag, "article_id")

            synced_slugs.append(slug)

    # 删除 DB 中存在但 content 目录中已不存在的文章
    all_db_articles = db.query(Article).all()
    for article in all_db_articles:
        if article.slug not in synced_slugs:
            db.query(ArticleTag).filter(
                ArticleTag.article_id == article.id
            ).delete()
            db.delete(article)
            logger.info("删除不存在的文章: %s", article.slug)

    db.commit()

    total = created + updated
    logger.info(
        "文章同步完成: 共 %d 篇 (新增 %d, 更新 %d, 跳过 %d)",
        total, created, updated, skipped,
    )
    return {
        "synced": total,
        "created": created,
        "updated": updated,
        "skipped": skipped,
    }


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
    """根据 slug（文件路径）获取已发布文章 + 内容"""
    article = (
        db.query(Article).filter(Article.slug == slug, Article.status == 1).first()
    )
    if not article:
        raise NotFoundError("文章")
    result = _article_to_dict(db, article)
    # 读取 content，剥离 frontmatter
    raw = _read_article_content(slug)
    if raw:
        _, body = _parse_frontmatter(raw)
        result["content"] = body
    else:
        result["content"] = None
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
            slug = f"{category_path}/{md_file[:-3]}"
            article = (
                db.query(Article)
                .filter(Article.slug == slug, Article.status == 1)
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
                        "slug": slug,
                        "title": md_file[:-3],
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
    file_path = _get_content_file_path(article.slug)
    dir_path = os.path.dirname(file_path)
    os.makedirs(dir_path, exist_ok=True)

    file_content = content
    if not content.strip().startswith("#"):
        file_content = f"# {article.title}\n\n{content}"

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
    file_path = _get_content_file_path(article.slug)
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
