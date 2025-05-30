# NayukiWeb - 个人作品集与知识管理系统

一个基于 FastAPI + Vue.js 的全栈Web应用，包含个人作品展示、文章管理、工具资源等功能。

[项目链接]:https://github.com/NayeyYe/NayukiWeb.git


## 🚀 技术栈

### 后端

- **FastAPI** - 高性能 Python Web 框架
- **SQLAlchemy** - Python SQL 工具包和 ORM
- **SQLite** - 轻量级数据库
- **Pydantic** - 数据验证和设置管理

### 前端

- **Vue 3** - 渐进式 JavaScript 框架
- **Vite** - 下一代前端构建工具
- **Element Plus** - Vue 3 组件库
- **Pinia** - Vue 状态管理
- **Vue Router** - Vue 官方路由
- **Axios** - HTTP 客户端

## 📦 项目结构

```
NayukiWeb/
├── app/                    # FastAPI 后端应用
│   ├── crud/              # 数据库操作层
│   │   ├── admin.py       # 管理员 CRUD 操作
│   │   ├── articles.py    # 文章 CRUD 操作
│   │   ├── books.py       # 书籍 CRUD 操作
│   │   ├── figures.py     # 人物 CRUD 操作
│   │   ├── projects.py    # 项目 CRUD 操作
│   │   ├── timeline.py    # 时间线 CRUD 操作
│   │   └── tools.py       # 工具 CRUD 操作
│   ├── __init__.py
│   ├── database.py        # 数据库配置
│   ├── init_db.py         # 数据库初始化
│   ├── main.py            # FastAPI 主应用
│   └── schemas.py         # Pydantic 模型定义
├── db/                    # 数据库相关文件
│   └── create_table.sql   # 建表语句
├── frontend/              # Vue.js 前端应用
│   ├── src/
│   │   ├── components/    # Vue 组件
│   │   │   ├── Admin/     # 管理后台组件
│   │   │   └── Main/      # 主站组件
│   │   ├── router/        # 路由配置
│   │   ├── views/         # 页面视图
│   │   ├── App.vue        # 根组件
│   │   └── main.js        # 入口文件
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── requirements.txt       # Python 依赖
└── README.md
```

## 🛠️ 安装与运行

### 前提条件

- Python 3.9
- Node.js 22.19.0
- npm 11.6.0

### 后端设置

1. 安装 Python 依赖：

```bash
pip install -r requirements.txt
```

2. 初始化数据库：

```bash
python app/init_db.py
```

3. 启动后端服务器：

```bash
uvicorn app.main:app --port 8080
```

后端服务将在 http://localhost:8000 运行

### 前端设置

1. 进入前端目录：

```bash
cd frontend
```

2. 安装依赖：

```bash
npm install
```

3. 启动开发服务器：

```bash
npm run dev
```

前端服务将在 http://localhost:5173 运行

## 📡 API 接口

### 文章相关

- `GET /articles/` - 获取文章列表
- `GET /articles/{article_id}` - 获取特定文章

### 项目相关

- `GET /projects/` - 获取项目列表
- `GET /projects/{project_id}` - 获取特定项目

### 工具相关

- `GET /tools/` - 获取工具列表
- `GET /tools/{tool_id}` - 获取特定工具

### 其他资源

- 书籍管理
- 人物资源
- 时间线事件
- 收藏图片

## 🎯 功能特性

### 前台功能

- **首页** - 个人简介和时间线展示
- **文章** - 技术文章和博客内容
- **项目** - 个人项目作品展示
- **资源** - 书籍和人物资源库
- **工具** - 实用工具推荐

### 后台管理

- **文章管理** - CRUD 操作和分类过滤
- **项目管理** - 项目上传和编辑
- **资源管理** - 书籍和人物资源管理
- **仪表盘** - 时间线和收藏图片编辑

## 🔧 开发说明

### 数据库模型

项目使用 SQLAlchemy ORM，主要数据模型包括：

- Articles (文章)
- Projects (项目)
- Tools (工具)
- Books (书籍)
- Figures (人物)
- TimelineEvents (时间线事件)
- FavoriteImages (收藏图片)

### 前端路由

- `/` - 首页
- `/about` - 关于我
- `/articles` - 文章列表
- `/projects` - 项目列表
- `/resources` - 资源页面
- `/tools` - 工具页面
- `/admin` - 管理后台

## 📝 部署说明

### 生产环境构建

后端：

```bash
uvicorn app.main:app --port 8080
```

前端：

```bash
cd frontend
npm i
npm run build
```

构建后的文件在 `frontend/dist/` 目录中

## 🙏 致谢

- [FastAPI](https://fastapi.tiangolo.com/)
- [Vue.js](https://vuejs.org/)
- [Element Plus](https://element-plus.org/)
- [Vite](https://vitejs.dev/)
