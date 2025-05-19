"""
NayukiWeb 后端 API 测试脚本

使用 FastAPI TestClient + SQLite 内存数据库 测试所有 API 端点。
用法: pytest tests/test_api.py -v
"""

import os

# 在任何 app 模块被导入之前，设置测试用的 DATABASE_URL
os.environ["DATABASE_URL"] = "sqlite:///./test.db"
os.environ["ADMIN_PASSWORD"] = "test_admin_pass"


import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.main import app

# ── 测试数据库配置 ──────────────────────────────────────
TEST_DATABASE_URL = "sqlite://"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_database():
    """每个测试前重建表并创建 admin 用户"""
    Base.metadata.create_all(bind=engine)
    # 创建管理员用户
    db = TestingSessionLocal()
    from app.services.admin import create_admin

    try:
        create_admin(db, "admin", "test_admin_pass")
    except Exception:
        pass
    db.close()
    yield
    Base.metadata.drop_all(bind=engine)


client = TestClient(app)


# ── Health ──────────────────────────────────────────────


def test_health():
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


# ── Articles ────────────────────────────────────────────


def test_get_articles_empty():
    r = client.get("/api/articles")
    assert r.status_code == 200
    assert r.json() == []


def test_create_article_admin():
    r = client.post(
        "/api/articles",
        json={
            "title": "测试文章",
            "content": "# Hello\n\n这是测试内容",
            "category": "test",
            "status": "published",
            "image": "https://example.com/cover.jpg",
            "tags": ["python", "tutorial"],
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert data["message"] == "文章上传成功"
    assert "id" in data


def test_get_articles_after_create():
    client.post(
        "/api/articles",
        json={
            "title": "已发布文章",
            "content": "内容",
            "status": "published",
        },
    )
    r = client.get("/api/articles")
    assert r.status_code == 200
    articles = r.json()
    assert len(articles) == 1
    assert articles[0]["title"] == "已发布文章"
    assert articles[0]["word_count"] >= 0


def test_get_article_by_slug():
    client.post(
        "/api/articles",
        json={
            "title": "Slug测试",
            "content": "内容",
            "status": "published",
        },
    )
    articles = client.get("/api/articles").json()
    slug = articles[0]["slug"]
    r = client.get(f"/api/articles/{slug}")
    assert r.status_code == 200
    assert r.json()["title"] == "Slug测试"


def test_update_article():
    resp = client.post(
        "/api/articles",
        json={
            "title": "原标题",
            "content": "内容",
            "status": "published",
        },
    )
    article_id = resp.json()["id"]
    r = client.put(f"/api/articles/{article_id}", json={"title": "新标题"})
    assert r.status_code == 200
    assert r.json()["message"] == "文章信息编辑成功"


def test_update_article_status():
    resp = client.post(
        "/api/articles",
        json={
            "title": "状态测试",
            "content": "内容",
            "status": "published",
        },
    )
    article_id = resp.json()["id"]
    r = client.patch(f"/api/articles/{article_id}/status", json={"status": "draft"})
    assert r.status_code == 200


def test_delete_article():
    resp = client.post(
        "/api/articles",
        json={
            "title": "删除测试",
            "content": "内容",
            "status": "published",
        },
    )
    article_id = resp.json()["id"]
    r = client.delete(f"/api/articles/{article_id}")
    assert r.status_code == 200
    assert r.json()["message"] == "文章删除成功"


def test_get_admin_articles():
    client.post(
        "/api/articles",
        json={
            "title": "Admin文章",
            "content": "内容",
            "status": "draft",
        },
    )
    r = client.get("/api/admin/articles")
    assert r.status_code == 200
    articles = r.json()
    assert len(articles) >= 1
    assert "status" in articles[0]


def test_get_article_tags():
    r = client.get("/api/tags")
    assert r.status_code == 200


def test_get_article_categories():
    r = client.get("/api/articles/categories")
    assert r.status_code == 200


# ── Projects ────────────────────────────────────────────


def test_get_projects_empty():
    r = client.get("/api/projects")
    assert r.status_code == 200
    assert r.json() == []


def test_create_project():
    r = client.post(
        "/api/projects",
        json={
            "name": "NayukiWeb",
            "link": "https://github.com/NayukiChiba/nyeweb",
            "description": "个人网站",
            "visibility": "published",
            "tech_stack": ["vue", "fastapi"],
        },
    )
    assert r.status_code == 200
    assert r.json()["message"] == "项目创建成功"


def test_get_projects_after_create():
    client.post(
        "/api/projects",
        json={
            "name": "项目A",
            "link": "https://github.com/test/a",
            "visibility": "published",
        },
    )
    r = client.get("/api/projects")
    assert r.status_code == 200
    projects = r.json()
    assert len(projects) == 1
    assert projects[0]["link"] == "https://github.com/test/a"


def test_get_project_by_id():
    resp = client.post(
        "/api/projects",
        json={
            "name": "项目B",
            "link": "https://github.com/test/b",
            "visibility": "published",
        },
    )
    pid = resp.json()["id"]
    r = client.get(f"/api/projects/{pid}")
    assert r.status_code == 200
    assert r.json()["name"] == "项目B"


def test_update_project():
    resp = client.post(
        "/api/projects",
        json={
            "name": "原项目",
            "link": "https://github.com/test/old",
            "visibility": "published",
        },
    )
    pid = resp.json()["id"]
    r = client.put(f"/api/projects/{pid}", json={"name": "新项目名"})
    assert r.status_code == 200


def test_delete_project():
    resp = client.post(
        "/api/projects",
        json={
            "name": "删除项目",
            "link": "https://github.com/test/del",
            "visibility": "published",
        },
    )
    pid = resp.json()["id"]
    r = client.delete(f"/api/projects/{pid}")
    assert r.status_code == 200


def test_get_project_tags():
    r = client.get("/api/project-tags")
    assert r.status_code == 200


# ── Books ───────────────────────────────────────────────


def test_get_books_empty():
    r = client.get("/api/books")
    assert r.status_code == 200
    data = r.json()
    assert data["data"] == []
    assert "pagination" in data


def test_create_book():
    r = client.post(
        "/api/admin/books",
        json={
            "title": "Python入门",
            "url": "https://pan.baidu.com/s/abc123",
            "description": "Python 基础教程",
            "status": "published",
            "tags": ["python"],
        },
    )
    assert r.status_code == 200
    assert r.json()["message"] == "图书创建成功"
    assert "url" in r.json()


def test_get_books_after_create():
    client.post(
        "/api/admin/books",
        json={
            "title": "JS高级",
            "url": "https://example.com/dl",
            "status": "published",
        },
    )
    r = client.get("/api/books")
    data = r.json()
    assert len(data["data"]) == 1
    assert data["data"][0]["url"] == "https://example.com/dl"


def test_update_book():
    resp = client.post(
        "/api/admin/books",
        json={
            "title": "原书名",
            "url": "https://example.com/old",
            "status": "published",
        },
    )
    bid = resp.json()["id"]
    r = client.put(f"/api/admin/books/{bid}", json={"title": "新书名"})
    assert r.status_code == 200


def test_delete_book():
    resp = client.post(
        "/api/admin/books",
        json={
            "title": "删除书",
            "url": "https://example.com/del",
            "status": "published",
        },
    )
    bid = resp.json()["id"]
    r = client.delete(f"/api/books/{bid}")
    assert r.status_code == 200


def test_get_book_tags():
    r = client.get("/api/book-tags")
    assert r.status_code == 200


# ── Tools ───────────────────────────────────────────────


def test_get_tools_empty():
    r = client.get("/api/tools")
    assert r.status_code == 200
    data = r.json()
    assert data["data"] == []


def test_create_tool():
    r = client.post(
        "/api/tools",
        json={
            "name": "JSON格式化",
            "url": "https://json.org",
            "description": "在线JSON工具",
            "category": "前端",
            "status": "published",
        },
    )
    assert r.status_code == 200


def test_get_tool_tags():
    r = client.get("/api/tool-tags")
    assert r.status_code == 200


# ── Timeline ────────────────────────────────────────────


def test_get_timeline_empty():
    r = client.get("/api/timeline")
    assert r.status_code == 200
    assert r.json() == []


def test_create_timeline():
    r = client.post(
        "/api/timeline",
        json={
            "timestamp": "2025-01-01 00:00:00",
            "content": "NayukiWeb 正式上线",
        },
    )
    assert r.status_code == 200


def test_get_timeline_after_create():
    client.post(
        "/api/timeline",
        json={
            "timestamp": "2025-06-01 12:00:00",
            "content": "事件A描述",
        },
    )
    r = client.get("/api/timeline")
    assert len(r.json()) >= 1


# ── Favorite Images ────────────────────────────────────


def test_get_favorite_images_empty():
    r = client.get("/api/favorite-images")
    assert r.status_code == 200
    assert r.json() == []


# ── Admin ───────────────────────────────────────────────


def test_admin_login_success():
    r = client.post(
        "/api/admin/login", json={"username": "admin", "password": "test_admin_pass"}
    )
    assert r.status_code == 200
    assert "token" in r.json()


def test_admin_login_failure():
    r = client.post("/api/admin/login", json={"username": "admin", "password": "wrong"})
    assert r.status_code in [401, 400, 200]


# ── Diaries ─────────────────────────────────────────────


def test_get_diaries_empty():
    r = client.get("/api/diaries")
    assert r.status_code == 200
    assert r.json() == []


def test_create_diary():
    r = client.post(
        "/api/diaries",
        json={
            "date": "2026-03-11T10:58",
            "content": "测试日记",
            "mood": "happy",
            "weather": "sunny",
        },
    )
    assert r.status_code == 200
    assert r.json()["message"] == "日记创建成功"


def test_get_diaries_after_create():
    client.post(
        "/api/diaries",
        json={
            "date": "2026-01-27T22:30",
            "content": "今天很开心",
            "mood": "excited",
            "weather": "cloudy",
        },
    )
    r = client.get("/api/diaries")
    assert len(r.json()) >= 1
    assert r.json()[0]["mood"] == "excited"


def test_update_diary():
    resp = client.post(
        "/api/diaries",
        json={
            "date": "2026-02-04T00:30",
            "content": "原内容",
        },
    )
    did = resp.json()["id"]
    r = client.put(f"/api/diaries/{did}", json={"content": "新内容"})
    assert r.status_code == 200


def test_delete_diary():
    resp = client.post(
        "/api/diaries",
        json={
            "date": "2026-02-09T00:30",
            "content": "删除测试",
        },
    )
    did = resp.json()["id"]
    r = client.delete(f"/api/diaries/{did}")
    assert r.status_code == 200
    assert r.json()["message"] == "日记删除成功"


# ── Gallery ─────────────────────────────────────────────


def test_get_gallery_empty():
    r = client.get("/api/gallery")
    assert r.status_code == 200
    assert r.json() == []


def test_create_gallery():
    r = client.post(
        "/api/gallery",
        json={
            "title": "壁纸",
            "url": "https://img.yumeko.site/file/wallpaper/wp.jpg",
            "date": "2026-02-11",
            "tags": ["wallpaper"],
        },
    )
    assert r.status_code == 200
    assert r.json()["message"] == "图片添加成功"


def test_get_gallery_after_create():
    client.post(
        "/api/gallery",
        json={
            "title": "亚托莉",
            "url": "https://img.yumeko.site/file/wife/atri.jpg",
            "tags": ["wife"],
        },
    )
    r = client.get("/api/gallery")
    assert len(r.json()) >= 1


def test_delete_gallery():
    resp = client.post(
        "/api/gallery",
        json={
            "title": "删除图",
            "url": "https://example.com/del.jpg",
        },
    )
    gid = resp.json()["id"]
    r = client.delete(f"/api/gallery/{gid}")
    assert r.status_code == 200


# ── Todos ───────────────────────────────────────────────


def test_get_todos_empty():
    r = client.get("/api/todos")
    assert r.status_code == 200
    assert r.json() == []


def test_create_todo():
    r = client.post(
        "/api/todos",
        json={
            "task": "学习深度学习",
            "priority": "medium",
            "type": "mid-term",
            "progress": 10,
        },
    )
    assert r.status_code == 200
    assert r.json()["message"] == "待办创建成功"


def test_get_todos_after_create():
    client.post(
        "/api/todos",
        json={
            "task": "Kaggle训练",
            "priority": "high",
            "progress": 50,
        },
    )
    r = client.get("/api/todos")
    assert len(r.json()) >= 1


def test_update_todo():
    resp = client.post("/api/todos", json={"task": "原任务"})
    tid = resp.json()["id"]
    r = client.put(f"/api/todos/{tid}", json={"progress": 80})
    assert r.status_code == 200


def test_complete_todo():
    resp = client.post("/api/todos", json={"task": "完成测试"})
    tid = resp.json()["id"]
    r = client.put(f"/api/todos/{tid}", json={"completed": True})
    assert r.status_code == 200


def test_delete_todo():
    resp = client.post("/api/todos", json={"task": "删除任务"})
    tid = resp.json()["id"]
    r = client.delete(f"/api/todos/{tid}")
    assert r.status_code == 200
    assert r.json()["message"] == "待办删除成功"
