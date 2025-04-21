"""
应用配置管理 — 基于 pydantic-settings，从 .env 自动加载
"""

import os
from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """应用全局配置"""

    # 数据库
    DATABASE_URL: str

    # 管理员
    ADMIN_PASSWORD: str = ""

    # CORS
    CORS_ORIGINS: list[str] = [
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    # 应用
    APP_TITLE: str = "NayukiWeb API"
    APP_VERSION: str = "2.0.0"
    DEBUG: bool = False

    # 前端 dist 路径（相对于项目根）
    FRONTEND_DIST_DIR: str = "frontend/dist"
    FRONTEND_PUBLIC_DIR: str = "frontend/public"

    # 文章内容目录（相对于项目根）
    CONTENT_DIR: str = "content/blog"

    model_config = {
        "env_file": os.path.join(
            os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            ),
            ".env",
        ),
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
        "extra": "ignore",
    }

    @property
    def project_root(self) -> str:
        """项目根目录"""
        return os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )

    @property
    def dist_dir(self) -> str:
        """前端构建产物绝对路径"""
        return os.path.join(self.project_root, self.FRONTEND_DIST_DIR)

    @property
    def public_dir(self) -> str:
        """前端 public 绝对路径"""
        return os.path.join(self.project_root, self.FRONTEND_PUBLIC_DIR)

    @property
    def content_dir(self) -> str:
        """文章内容绝对路径"""
        return os.path.join(self.project_root, self.CONTENT_DIR)


@lru_cache
def get_settings() -> Settings:
    """获取全局配置（单例）"""
    return Settings()
