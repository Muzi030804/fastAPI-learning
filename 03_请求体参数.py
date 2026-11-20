from fastapi import FastAPI
from pydantic import BaseModel,Field
app = FastAPI()
@app.get("/")
async def root():
    return {"message": "Hello World"}

# 注册: 用户名和密码 ->str
class User(BaseModel):
    username: str = Field(default="张三",min_length=2,max_length=10,description="用户名,2-10字")
    password: str = Field(min_length=3,max_length=20)

# 需求: 设计接口新增图书,图书信息包含: 书名,作者,出版社,售价
"""
具体要求如下:
书名：不能为空；长度 2 ~ 20
作者：长度 2 ~ 10
出版社：默认值“黑马出版社”
售价：不能为空；价格大于0元
"""

class Book(BaseModel):
    book_name: str = Field(...,min_length=2,max_length=20)
    book_author: str = Field(min_length=2,max_length=10)
    book_publication: str = Field(default="出版社")
    book_price: int = Field(...,gt=0)

@app.post("/book")
async def create_book(book: Book):
    return book

@app.post("/register")
async def register_user(user: User):
    return user
