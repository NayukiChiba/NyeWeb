# NayukiWeb

基于 **FastAPI** + **Vue 3** 的个人博客与作品集系统。

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | FastAPI · SQLAlchemy · PostgreSQL · Pydantic |
| 前端 | Vue 3 · Vite · Element Plus · Tailwind CSS |
| 基础设施 | Uvicorn · Axios · Vue Router |

## 项目结构

```
NayukiWeb/
├── app/                     # FastAPI 后端
│   ├── api/v1/              # REST 接口（文章、项目、工具等）
│   ├── models/              # SQLAlchemy ORM 模型
│   ├── schemas/             # Pydantic 请求/响应模型
│   ├── services/            # 业务逻辑层
│   ├── core/                # 配置、认证、依赖注入
│   ├── main.py              # 应用入口 & 中间件
│   └── init_db.py           # 数据库初始化
├── frontend/                # Vue 3 单页应用
│   └── src/
│       ├── views/           # 页面组件（用户端 + 管理端）
│       ├── components/      # 可复用 UI 组件
│       ├── router/          # Vue Router 路由配置
│       └── assets/          # Tailwind CSS、静态资源
├── content/                 # Markdown 博客文章（自动同步）
├── db/                      # SQL 迁移脚本
├── tests/                   # Pytest 测试
└── requirements.txt
```

## 快速开始

### 后端

```bash
pip install -r requirements.txt
python app/init_db.py          # 仅首次运行
uvicorn app.main:app --port 8000 --reload
```

### 前端

```bash
cd frontend
npm install
npm run dev                    # → http://localhost:5173
```

## 功能

**用户端**
- 首页 — GitHub 活动图、最新文章/项目/日记
- 文章 — Markdown 博客，支持 KaTeX 公式、Mermaid 图表、代码高亮
- 项目 — 可筛选的作品集，技术标签
- 资源 — 图书 & 图片画廊
- 工具 — 实用工具推荐
- 关于 — 个人名片、技能、项目 Git 时间线

**管理端** (`/admin`)
- 所有模块的卡片式 CRUD（文章、项目、工具、资源、日记、待办）
- 文章从 `content/` 目录同步（POST `/api/articles/sync`）
- 控制台统计概览 & 收藏图片编辑

## 主要 API

| 方法 | 接口 | 说明 |
|------|------|------|
| GET | `/api/articles` | 文章列表 |
| POST | `/api/articles/sync` | 从 content/ 同步文章 |
| GET | `/api/projects` | 项目列表 |
| GET | `/api/tools` | 工具列表 |
| GET | `/api/diaries` | 日记列表 |
| GET | `/api/books` | 图书列表 |
| GET | `/api/figures` | 图片列表 |

## 许可

MIT
