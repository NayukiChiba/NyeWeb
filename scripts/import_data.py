"""
从 data/*.json 导入数据到 PostgreSQL

用法: python scripts/import_data.py
"""

import json
import os
import sys
from datetime import datetime

# 确保项目根目录在 sys.path
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from sqlalchemy.orm import Session
from app.core.database import engine, SessionLocal, Base
from app.models import (
    Article,
    Project,
    Book,
    Tool,
    Diary,
    Gallery,
    Todo,
    Tag,
    ArticleTag,
    ProjectTag,
    BookTag,
    Admin,
)
from app.core.security import hash_password

DATA_DIR = os.path.join(ROOT, "data")


def load_json(filename: str):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        print(f"  ⚠ {filename} 不存在，跳过")
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def ensure_tag(db: Session, name: str) -> int:
    tag = db.query(Tag).filter(Tag.name == name).first()
    if not tag:
        tag = Tag(name=name)
        db.add(tag)
        db.flush()
    return tag.id


def import_articles(db: Session):
    data = load_json("articles.json")
    if not data:
        return
    items = data.get("articles", [])
    print(f"  导入 {len(items)} 篇文章...")
    for item in items:
        article_date = None
        if item.get("date"):
            try:
                article_date = datetime.strptime(item["date"], "%Y-%m-%d").date()
            except ValueError:
                pass
        slug = item.get("slug", item["title"].lower().replace(" ", "-"))
        status = 1 if item.get("status") == "published" else 0
        article = Article(
            title=item["title"],
            slug=slug,
            category=item.get("category"),
            date=article_date,
            description=item.get("description"),
            image=item.get("image"),
            status=status,
        )
        db.add(article)
        db.flush()
        for tag_name in item.get("tags", []):
            tag_id = ensure_tag(db, tag_name)
            db.add(ArticleTag(article_id=article.id, tag_id=tag_id))


def import_projects(db: Session):
    data = load_json("projects.json")
    if not data:
        return
    items = data.get("projects", [])
    print(f"  导入 {len(items)} 个项目...")
    for item in items:
        visibility = 1 if item.get("visibility") == "published" else 0
        project = Project(
            name=item["name"],
            description=item.get("description"),
            link=item["link"],
            tech_stack=item.get("techStack", []),
            status=item.get("status", "planning"),
            visibility=visibility,
        )
        db.add(project)
        db.flush()
        for tag_name in item.get("techStack", []):
            tag_id = ensure_tag(db, tag_name)
            db.add(ProjectTag(project_id=project.id, tag_id=tag_id))


def import_books(db: Session):
    data = load_json("books.json")
    if not data:
        return
    items = data.get("books", [])
    print(f"  导入 {len(items)} 本书籍...")
    for item in items:
        status = 1 if item.get("status") == "published" else 0
        book = Book(
            title=item["title"],
            cover=item.get("cover"),
            url=item["url"],
            status=status,
        )
        db.add(book)
        db.flush()
        for tag_name in item.get("tags", []):
            tag_id = ensure_tag(db, tag_name)
            db.add(BookTag(book_id=book.id, tag_id=tag_id))


def import_tools(db: Session):
    data = load_json("tools.json")
    if not data:
        return
    items = data.get("tools", [])
    print(f"  导入 {len(items)} 个工具...")
    for item in items:
        status = 1 if item.get("status") == "published" else 0
        tool = Tool(
            name=item["name"],
            description=item.get("description"),
            url=item.get("url"),
            icon=item.get("icon"),
            category=item.get("category"),
            status=status,
        )
        db.add(tool)


def import_diaries(db: Session):
    data = load_json("diaries.json")
    if not data:
        return
    items = data.get("diaries", [])
    print(f"  导入 {len(items)} 篇日记...")
    for item in items:
        dt = None
        if item.get("date"):
            try:
                dt = datetime.strptime(item["date"], "%Y-%m-%dT%H:%M")
            except ValueError:
                pass
        diary = Diary(
            date=dt,
            content=item["content"],
            mood=item.get("mood"),
            weather=item.get("weather"),
            images=item.get("images", []),
        )
        db.add(diary)


def import_gallery(db: Session):
    data = load_json("gallery.json")
    if not data:
        return
    items = data.get("gallery", [])
    print(f"  导入 {len(items)} 张图片...")
    for item in items:
        gallery_date = None
        if item.get("date"):
            try:
                gallery_date = datetime.strptime(item["date"], "%Y-%m-%d").date()
            except ValueError:
                pass
        status = 1 if item.get("status") == "published" else 0
        gallery = Gallery(
            title=item["title"],
            url=item["url"],
            date=gallery_date,
            tags=item.get("tags", []),
            status=status,
        )
        db.add(gallery)


def import_todos(db: Session):
    data = load_json("todos.json")
    if not data:
        return
    items = data.get("todos", [])
    print(f"  导入 {len(items)} 个待办...")
    for item in items:
        todo = Todo(
            task=item["task"],
            completed=item.get("completed", False),
            priority=item.get("priority", "medium"),
            type=item.get("type", "short-term"),
            progress=item.get("progress", 0),
            icon=item.get("icon"),
            status=item.get("status", "active"),
        )
        db.add(todo)


def create_admin(db: Session):
    """创建默认管理员"""
    existing = db.query(Admin).filter(Admin.username == "admin").first()
    if not existing:
        from app.core.config import get_settings

        settings = get_settings()
        pwd = settings.ADMIN_PASSWORD or "admin123"
        admin = Admin(username="admin", password_hash=hash_password(pwd))
        db.add(admin)
        print("  创建管理员 admin")


def main():
    print("=" * 50)
    print("NayukiWeb 数据导入脚本")
    print("=" * 50)

    # 1. 重建所有表
    print("\n[1/2] 重建数据库表...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("  ✓ 数据库表已重建")

    # 2. 导入数据
    print("\n[2/2] 导入 data/*.json 数据...")
    db = SessionLocal()
    try:
        import_articles(db)
        import_projects(db)
        import_books(db)
        import_tools(db)
        import_diaries(db)
        import_gallery(db)
        import_todos(db)
        create_admin(db)
        db.commit()
        print("\n✓ 所有数据导入完成！")

        # 统计
        print("\n--- 数据统计 ---")
        print(f"  文章: {db.query(Article).count()}")
        print(f"  项目: {db.query(Project).count()}")
        print(f"  书籍: {db.query(Book).count()}")
        print(f"  工具: {db.query(Tool).count()}")
        print(f"  日记: {db.query(Diary).count()}")
        print(f"  图库: {db.query(Gallery).count()}")
        print(f"  待办: {db.query(Todo).count()}")
        print(f"  标签: {db.query(Tag).count()}")

    except Exception as e:
        db.rollback()
        print(f"\n✗ 导入失败: {e}")
        import traceback

        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    main()
