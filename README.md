# YSJ Project

## 项目概述 | Project Overview

这是一个基于 Vue.js 和 Flask 的全栈应用程序，提供实时通信和用户管理功能。

This is a full-stack application based on Vue.js and Flask, providing real-time communication and user management features.

## 技术栈 | Tech Stack

### 前端 | Frontend
- Vue.js 2.x
- Vuex (状态管理)
- Vue Router
- Element UI
- Axios (HTTP 客户端)

### 后端 | Backend
- Python 3.x
- Flask (Web 框架)
- SQLAlchemy (ORM)
- Flask-SocketIO (WebSocket)
- Gunicorn (WSGI 服务器)

## 项目结构 | Project Structure

```
.
├── frontend/                # 前端项目目录
│   ├── src/                # 源代码
│   │   ├── api/           # API 接口
│   │   ├── assets/        # 静态资源
│   │   ├── components/    # 组件
│   │   ├── router/        # 路由配置
│   │   ├── store/         # Vuex 状态管理
│   │   └── views/         # 页面视图
│   └── public/            # 公共资源
│
└── y5-backend-flask/       # 后端项目目录
    ├── blueprints/        # 蓝图模块
    ├── entity/           # 实体类
    ├── sql/              # SQL 脚本
    ├── static/           # 静态文件
    ├── templates/        # 模板文件
    ├── app.py           # 主应用入口
    ├── config.py        # 配置文件
    ├── models.py        # 数据模型
    └── service.py       # 业务逻辑
```

## 功能特性 | Features

- 用户认证和授权
- 实时消息通信
- 房间管理
- 邮件通知
- RESTful API
- WebSocket 支持

## 开发环境设置 | Development Setup

### 前端 | Frontend
```bash
cd frontend
yarn install
yarn serve
```

### 后端 | Backend
```bash
cd y5-backend-flask
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

## API 文档 | API Documentation

API 文档可通过 Swagger UI 访问：`http://localhost:5000/swagger`

## 部署 | Deployment

### 前端部署 | Frontend Deployment
```bash
cd frontend
yarn build
```

### 后端部署 | Backend Deployment
```bash
cd y5-backend-flask
gunicorn -c gunicorn.py app:app
```

## 贡献指南 | Contributing

1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证 | License

[MIT License](LICENSE)
