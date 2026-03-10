"""
NayukiWeb FastAPI 应用入口
"""

import logging
import mimetypes
import os
from contextlib import asynccontextmanager
from urllib.parse import unquote

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.core.config import get_settings
from app.core.exceptions import register_exception_handlers
from app.api.v1 import router as api_v1_router

# 配置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(name)s] %(levelname)s: %(message)s"
)
logger = logging.getLogger("app")

settings = get_settings()


# ── Lifespan ────────────────────────────────────────────────


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("NayukiWeb API 启动, version=%s", settings.APP_VERSION)
    logger.info("Dist 目录: %s", settings.dist_dir)

    # 启动时同步 content/blog/ 文章到数据库
    from app.core.database import SessionLocal
    from app.services.article import sync_articles_from_content
    try:
        db = SessionLocal()
        result = sync_articles_from_content(db)
        logger.info("文章同步结果: %s", result)
        db.close()
    except Exception as e:
        logger.error("文章同步失败: %s", e)

    yield
    logger.info("NayukiWeb API 关闭")


# ── 创建应用 ────────────────────────────────────────────────

app = FastAPI(
    title=settings.APP_TITLE,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS + ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册异常处理器
register_exception_handlers(app)

# 注册 API 路由
app.include_router(api_v1_router)


# 健康检查
@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "API服务正常运行"}


# ── 静态文件 & SPA Fallback ────────────────────────────────

dist_dir = settings.dist_dir
static_assets_dir = os.path.join(dist_dir, "assets")

if os.path.exists(static_assets_dir):
    app.mount("/assets", StaticFiles(directory=static_assets_dir), name="assets")

if os.path.exists(dist_dir):
    app.mount("/static", StaticFiles(directory=dist_dir), name="dist")


@app.get("/{path:path}")
async def serve_vue_app(path: str):
    decoded_path = unquote(path)

    # 根路径
    if not decoded_path:
        index_html = os.path.join(dist_dir, "index.html")
        if os.path.exists(index_html):
            return FileResponse(index_html)
        raise HTTPException(status_code=404, detail="Frontend not built")

    # 尝试直接返回文件
    normalized = decoded_path.replace("/", os.sep)
    file_path = os.path.join(dist_dir, normalized)

    if os.path.exists(file_path) and os.path.isfile(file_path):
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type is None:
            ext = file_path.lower()
            if ext.endswith(".pdf"):
                mime_type = "application/pdf"
            elif ext.endswith(".md"):
                mime_type = "text/markdown"
            else:
                mime_type = "application/octet-stream"
        return FileResponse(
            path=file_path, media_type=mime_type, filename=os.path.basename(file_path)
        )

    # 尝试添加 .pdf 扩展名
    if not decoded_path.endswith(".pdf"):
        pdf_path = os.path.join(dist_dir, normalized + ".pdf")
        if os.path.exists(pdf_path) and os.path.isfile(pdf_path):
            return FileResponse(
                path=pdf_path,
                media_type="application/pdf",
                filename=os.path.basename(pdf_path),
            )

    # SPA fallback
    index_html = os.path.join(dist_dir, "index.html")
    if os.path.exists(index_html):
        return FileResponse(index_html)
    raise HTTPException(status_code=404, detail="File not found")


if __name__ == "__main__":
    uvicorn.run(app, port=8080)
