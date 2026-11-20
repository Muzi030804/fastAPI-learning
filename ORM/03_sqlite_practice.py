from  contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import String, select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker,AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# True：准备两名用户；False：准备空表
SEED_USERS = True

# 数据只保存在内存，不连接 MySQL，也不生成数据库文件
async_engine = create_async_engine(
    "sqlite+aiosqlite:///:memory:",
    echo=True
)

AsyncSessionLocal = async_sessionmaker(
    async_engine,
    expire_on_commit=False,
)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
    )

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        # 启动时创建测试表
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        # 准备测试数据，不是接口返回的硬编码答案
        if SEED_USERS:
            async with AsyncSessionLocal() as session:
                session.add_all([
                    User(id=1, user_name="alice"),
                    User(id=2, user_name="bob"),
                ])
                await session.commit()
        print("测试数据库已准备")
        yield
    finally:
        # 服务停止时释放数据库连接
        await async_engine.dispose()

app = FastAPI(lifespan=lifespan)

# 给接口提供数据库会话
async def get_ab():
    async with AsyncSessionLocal() as session:
        yield session

@app.get("/users")
async def get_users(db: AsyncSession = Depends(get_ab)):
    stmt = select(User)
    result = await db.execute(stmt)
    users = result.scalars().all()
    user_list = []
    for user in users:
        user_list.append({
            "id": user.id,
            "username": user.user_name,
        })
    return user_list

@app.get("/users/first")
async def get_first(db: AsyncSession = Depends(get_ab)):
    stmt = select(User)
    result = await db.execute(stmt)
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return {"id":user.id, "username": user.user_name}
