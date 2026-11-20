from fastapi import FastAPI
from fastapi.responses import HTMLResponse,FileResponse

app = FastAPI()
@app.get("/")
async def root():
    return {"message": "Hello World"}

# 两种使用响应类型的方式

# 接口 : 响应 HTML 代码 (直接在装饰器中指定响应类的方式)
@app.get("/html", response_class=HTMLResponse)
async def get_html():
    return "<h1>Hello World(一级标题)</h1>"

# 接口 : 返回图片内容 (采用返回对象的方式)
@app.get("/file")
async def get_file():
    path = "../06_streamlit_chat/resources/cat.jpg"
    return FileResponse(path)  # 采用返回对象的方式