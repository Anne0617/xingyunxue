# 星学堂 — 项目说明

## 项目概述

星学堂（Nebula Study）是一个在线学习管理平台，基于 Django + Vue 3 构建，采用前后端分离架构。

## 技术栈

| 层 | 技术 | 版本 |
|---|------|------|
| 后端框架 | Django | 6.0.6 |
| REST API | Django REST Framework | 3.17.1 |
| 管理后台 | SimpleUI | 2026.1.13 |
| 前端框架 | Vue 3 + Composition API | — |
| 构建工具 | Vite | 8.0+ |
| 数据库 | SQLite（开发） | — |
| CORS | django-cors-headers | 4.9.0 |
| 运行时 | Python 3.14 + Node.js 24 | — |

## 工作区结构

星云学/ 工作区包含两个项目：

星云学/
├── 星学堂/              # 新员工培训学习系统
├── 十五五打卡/           # 十五五规划闯关打卡
├── .venv/               # Python 虚拟环境
└── .gitignore

## 项目结构

星学堂/
├── star_course/             # 闯关前端（静态 HTML）
├── frontend/                # Vue 3 前端（管理后台）
│   ├── src/
│   │   ├── App.vue
│   │   ├── main.js
│   │   ├── style.css
│   │   └── views/
│   ├── dist/                # 构建产物
│   ├── vite.config.js
│   ├── index.html
│   └── package.json
├── nebula/                  # Django 项目配置
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py / asgi.py
├── learning/                # Django 应用
│   ├── views.py
│   ├── urls.py
│   ├── models.py
│   ├── admin.py
│   └── migrations/
├── manage.py
├── start.bat                # 快速启动脚本
├── Dockerfile               # Docker 部署
├── rail way.json            # Railway 部署
├── requirements.txt
└── agent.md

## 快速启动

### 1. 激活虚拟环境

.venv\Scripts\Activate.ps1

### 2. 启动 Django 服务

python manage.py runserver 127.0.0.1:8000

### 3. （可选）启动 Vue 开发服务器

cd frontend
npm run dev

### 4. 构建前端（修改 Vue 后需重新构建）

cd frontend
npm run build

## 服务地址

| 地址 | 说明 |
|------|------|
| http://127.0.0.1:8000/ | 前端首页 |
| http://127.0.0.1:8000/admin/ | 管理后台 |
| http://127.0.0.1:8000/api/ | API 接口 |
| http://127.0.0.1:5173/ | Vue 开发服务器 |

## 管理后台

| 项目 | 值 |
|------|------|
| 地址 | /admin/ |
| 用户名 | 星河智善总部 |
| 密码 | xhzs2026 |

## API 端点

- GET /api/health/ — 健康检查
- POST /api/feedback/ — 提交反馈
- POST /api/login/ — 登录
- GET /api/exams/ — 考试列表
- GET /api/exams/<slug>/ — 考试详情
- POST /api/exams/<slug>/submit/ — 提交答卷
- GET /api/exams/<slug>/results/ — 成绩统计
- GET /api/exams/<slug>/qrcode/ — 考试二维码
- GET /api/badges/ — 称号列表
- POST /api/badges/claim/ — 领取称号
- GET /api/announcements/ — 公告列表
- GET /api/download/<filename>/ — 文件下载

## 依赖管理

### Python

pip install -r requirements.txt

### 前端

cd frontend
npm install
