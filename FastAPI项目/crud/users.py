import uuid
from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from models.users import User, UserToken
from schemas.users import UserRequest, UserUpdateRequest
from utils import security


#根据用户名查询数据库
async def get_user_by_username(db:AsyncSession, username: str):
    query = select(User).where(User.username == username)
    result = await db.execute(query)
    return result.scalar_one_or_none()

# 创建用户
async def create_user(db:AsyncSession, user_data: UserRequest):
    # 先密码加密 -> add
    hashed_password = security.get_hash_password(user_data.password)
    user = User(username=user_data.username, password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user) # 从数据库读回最新的user
    return user

# 生成Token
async def create_token(db:AsyncSession, user_id: int):
    # 生成 Token+ 设置过期时间 -> 查询数据库当前用户是否有 Token -> 有: 更新, 没有: 添加
    token = str(uuid.uuid4())
    # timedelta(days=7, hours=2, minutes=30, seconds=10) 表示7天2小时30分10秒
    expires_at = datetime.now() + timedelta(days=7)
    query = select(UserToken).where(UserToken.user_id == user_id)
    result = await db.execute(query)
    user_token = result.scalar_one_or_none()

    if user_token:
        user_token.token = token
        user_token.expires_at = expires_at
    else:
        user_token = UserToken(user_id=user_id, token=token, expires_at=expires_at)  # 创建一个新的对象
        db.add(user_token)

    await db.commit()
    return token


# 验证用户登录

async def authenticate_user(db:AsyncSession, username: str, password: str):
    user = await get_user_by_username(db, username)
    if not user:
        return None
    # security.verify_password(password, user.password) 为 False 表示明文密码与输入密码不一致
    if not security.verify_password(password, user.password):
        return None

    return user

# 根据 Token 查询用户: 验证 Token -> 查询用户
async def get_user_by_token(db:AsyncSession, token: str):
    query = select(UserToken).where(UserToken.token == token)
    result = await db.execute(query)
    db_token = result.scalar_one_or_none()

    if not db_token or db_token.expires_at < datetime.now():
        return None

    query = select(User).where(User.id == db_token.user_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()

# 更新用户信息: update 更新 -> 检查是否命中 -> 获取更新后的用户返回
async def update_user(db:AsyncSession, username: str, user_data: UserUpdateRequest):
    # update(User).where(User.username == user_name).values(字段=值,字段=值,...)
    # user_data 是一个Pydantic类型, 得到字典 -> ** 解包
    # 用户没有设置的就不更新
    query = update(User).where(User.username == username).values(**user_data.model_dump(
        exclude_unset=True, # 只保留请求中显式提供的字段
        exclude_none=True,  # 排除值为 None 的字段（空字符串仍会保留）
    ))
    result = await db.execute(query)
    await db.commit()

    # 检查更新
    if result.rowcount == 0:
        raise HTTPException(status_code=404,detail="User not found")

    # 获取一下更新后的用户
    updated_user = await get_user_by_username(db, username)
    return updated_user

# 修改密码: 验证旧密码 -> 新密码加密 -> 修改密码
async def change_password(db: AsyncSession, user: User,old_password: str, new_password: str):
    if not security.verify_password(old_password, user.password):
        return False

    hashed_password = security.get_hash_password(new_password)
    user.password = hashed_password
    await db.commit()
    await db.refresh(user)
    return True
