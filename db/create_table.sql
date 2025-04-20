-- PostgreSQL 建表语句 (最终版)
-- NayukiWeb 数据库 — 字段对齐 data/*.json

-- 文章表
CREATE TABLE IF NOT EXISTS articles
(
    id          SERIAL PRIMARY KEY,
    title       VARCHAR(255) NOT NULL,
    slug        VARCHAR(255) NOT NULL UNIQUE,
    category    VARCHAR(100),
    date        DATE,
    description TEXT,                        -- 文章描述 (data: description)
    image       VARCHAR(2083),               -- 封面图URL (data: image)
    word_count  INTEGER DEFAULT 0,
    updated_at  TIMESTAMP,
    status      SMALLINT NOT NULL DEFAULT 1
);

-- 项目表 (链接形式)
CREATE TABLE IF NOT EXISTS projects
(
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(255)  NOT NULL,       -- data: name
    description TEXT,                         -- data: description
    link        VARCHAR(2083) NOT NULL,       -- data: link (GitHub)
    tech_stack  JSONB DEFAULT '[]',           -- data: techStack
    status      VARCHAR(50) DEFAULT 'planning', -- planning/in-progress/completed
    visibility  SMALLINT NOT NULL DEFAULT 1    -- 0=draft 1=published
);

-- 书籍表 (链接形式)
CREATE TABLE IF NOT EXISTS books
(
    id          SERIAL PRIMARY KEY,
    title       VARCHAR(255)  NOT NULL,
    description TEXT,
    cover       VARCHAR(500),
    url         VARCHAR(2083) NOT NULL,
    status      SMALLINT NOT NULL DEFAULT 1
);

-- 工具表
CREATE TABLE IF NOT EXISTS tools
(
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(255) NOT NULL,         -- data: name
    description TEXT,
    url         VARCHAR(2083),
    icon        TEXT,                           -- data: icon (SVG)
    category    VARCHAR(100),                   -- data: category
    status      SMALLINT NOT NULL DEFAULT 1
);

-- 日记表
CREATE TABLE IF NOT EXISTS diaries
(
    id       SERIAL PRIMARY KEY,
    date     TIMESTAMP NOT NULL,
    content  TEXT NOT NULL,
    mood     VARCHAR(50),                      -- happy/tired/neutral/excited
    weather  VARCHAR(50),                      -- sunny/cloudy/rainy
    images   JSONB DEFAULT '[]'
);

-- 图库表
CREATE TABLE IF NOT EXISTS gallery
(
    id     SERIAL PRIMARY KEY,
    title  VARCHAR(255) NOT NULL,
    url    VARCHAR(2083) NOT NULL,
    date   DATE,
    tags   JSONB DEFAULT '[]',
    status SMALLINT NOT NULL DEFAULT 1
);

-- 待办事项表
CREATE TABLE IF NOT EXISTS todos
(
    id        SERIAL PRIMARY KEY,
    task      VARCHAR(500) NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    priority  VARCHAR(50) DEFAULT 'medium',
    type      VARCHAR(50) DEFAULT 'short-term',
    progress  INTEGER DEFAULT 0,
    icon      TEXT,
    status    VARCHAR(50) DEFAULT 'active'
);

-- 时间线表
CREATE TABLE IF NOT EXISTS timeline
(
    id        SERIAL PRIMARY KEY,
    timestamp TIMESTAMP,
    content   TEXT NOT NULL
);

-- 收藏图片表
CREATE TABLE IF NOT EXISTS favorite_images
(
    id         SERIAL PRIMARY KEY,
    url        VARCHAR(2083) NOT NULL,
    alt_text   VARCHAR(255),
    sort_order INTEGER DEFAULT 0
);

-- 标签表
CREATE TABLE IF NOT EXISTS tags
(
    id   SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

-- 关联表
CREATE TABLE IF NOT EXISTS article_tags
(
    article_id INTEGER REFERENCES articles (id),
    tag_id     INTEGER REFERENCES tags (id),
    PRIMARY KEY (article_id, tag_id)
);

CREATE TABLE IF NOT EXISTS project_tags
(
    project_id INTEGER REFERENCES projects (id),
    tag_id     INTEGER REFERENCES tags (id),
    PRIMARY KEY (project_id, tag_id)
);

CREATE TABLE IF NOT EXISTS book_tags
(
    book_id INTEGER REFERENCES books (id),
    tag_id  INTEGER REFERENCES tags (id),
    PRIMARY KEY (book_id, tag_id)
);

CREATE TABLE IF NOT EXISTS tool_tags
(
    tool_id INTEGER REFERENCES tools (id),
    tag_id  INTEGER REFERENCES tags (id),
    PRIMARY KEY (tool_id, tag_id)
);

-- 管理员表
CREATE TABLE IF NOT EXISTS admins
(
    id            SERIAL PRIMARY KEY,
    username      VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    login_token   VARCHAR(255),
    last_login    TIMESTAMP
);
