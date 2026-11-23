# FastAPI 学习与实践

从 FastAPI 入门到工程化的练习代码，包含一个基于 FastAPI + SQLAlchemy + MySQL 的新闻资讯项目示例。

## 目录结构

| 路径 | 内容 |
| --- | --- |
| `01_FastAPI入门.py` ~ `08_依赖注入.py` | FastAPI 基础：路由、查询参数、请求体、响应模型、异常处理、中间件、依赖注入 |
| `ORM/` | SQLAlchemy 建表、SQLite 练习 |
| `CORS_demo/` | 跨域配置示例（后端 + 前端页面） |
| `FastAPI项目/` | 分层项目代码：`routers/`、`crud/`、`models/`、`schemas/`、`utils/`、`config/` |
| `FastAPI项目/项目物料/` | 接口规范文档、数据库 SQL、前端源码（`node_modules` 不入库） |

## 运行

```bash
cd FastAPI项目
pip install fastapi uvicorn sqlalchemy aiomysql
uvicorn main:app --reload
```

依赖：FastAPI、Uvicorn、SQLAlchemy、aiomysql（数据库连接配置见 `FastAPI项目/config/db_conf.py`，建议改为从环境变量读取）。

## 说明

- 代码为学习过程中的练习与项目实践，部分示例使用本地 MySQL 或 SQLite。
- `项目物料/` 中的前端工程需先执行 `npm install` 再启动。