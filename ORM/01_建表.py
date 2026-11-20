from datetime import datetime
from fastapi import FastAPI
from sqlalchemy import DateTime, func, String, Float, Integer
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

app = FastAPI()

# 1. 创建异步引擎
ASYNC_DATABASE_URL = "mysql+aiomysql://root:123456@localhost:3306/FastAPI_first"
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,     # 数据库地址
    echo=True,              # 可选, 输出 SQL 日志
    pool_size=10,           # 设置连接池活跃的连接数
    max_overflow=20,        # 允许额外的连接数
)

# 2. 定义模型类: 基类 + 表对应的模型类
# 基类: 创建时间, 更新时间; 书籍(类)表: id, 书名, 作者, 价格, 出版社
class Base(DeclarativeBase):
    create_time: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now(), default=func.now, comment="创建时间")
    update_time: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now(), default=func.now, onupdate=func.now(), comment="修改的时间")

class Book(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True, comment="书籍id")
    book_name: Mapped[str] = mapped_column(String(255), comment="书名")
    author: Mapped[str] = mapped_column(String(255), comment="作者")
    price: Mapped[float] = mapped_column(Float, comment="价格")
    publisher: Mapped[str] = mapped_column(String(255), comment="出版社")

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(255),nullable=False,unique=True)
    password: Mapped[str] = mapped_column(String(255),nullable=False)
    age: Mapped[int | None] = mapped_column(Integer)

# 3. 建表: 定义函数建表 -> FastAPI 启动的时候调用建表的函数
async def create_table():
    # 获取异步引擎, 创建事务 - 建表
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)   # Base 模型类的元数据创建

@app.on_event("startup")
async def startup_event():
    await create_table()




@app.get("/")
async def root():
    return {"message": "Hello World"}