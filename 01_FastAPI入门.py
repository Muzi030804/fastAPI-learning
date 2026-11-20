from fastapi import FastAPI,Path

# 创建FastAPI实例对象
app = FastAPI()

# 定义API接口, 该函数的返回值表示 API接口 的返回的数据, 接口访问路径为 / ,请求方式为GET
@app.get("/")
async def root():
    return {"message": "Hello World"}

# 定义API接口
@app.get("/users")
async def get_users():
    return [
        {"name": "Michael", "age": 25},
        {"name": "Ben", "age": 30},
        {"name": "Sarah", "age": 40},
    ]
@app.get("/hello")
async def hello():
    return {"message": "Hello World"}

@app.get("/users/{user_id}")
async def get_user(user_id: int = Path(..., gt=0,lt=101,description="用户的id,取值范围是1-100")):
    return {"user_id": user_id}

# 需求: 查找用户姓名,路径参数 name ,长度范围 2-10
@app.get("/user/{name}")
async def get_user_name(name:str = Path(...,min_length=2,max_length=10)):
    return {"名字是": name}

# 启动服务: uvicorn: Python中的轻量级Web服务器
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

