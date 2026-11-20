from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 这是允许访问后端的前端地址名单。必须与浏览器地址栏中的协议、主机和端口一致。
origins = ["http://127.0.0.1:5500"]

app.add_middleware(         # 将CORS中间件安装到FastAPI应用。以后请求进入接口之前，会先经过这个中间件。
    CORSMiddleware,
    allow_origins=origins,      # 只允许名单里的来源访问。
    allow_credentials=False,    # 当前实验不需要Cookie等身份凭证，所以设为 False。
    allow_methods=["GET"],      # 当前前端只发送GET请求，因此只允许GET。
    allow_headers=["*"],        # 允许前端使用各种请求头。
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/api/message")
async def get_message():
    return {"message": "FastAPI连接成功"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)