from fastapi import FastAPI,Query
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


# 需求: 查询新闻 -> 分页, skip: 跳过的记录数, limit: 返回的记录数 10
@app.get("/news/news_list")
async def get_news_list(
        skip: int = Query(0,description="跳过的记录数",lt=100),
        limit: int = Query(10,description="返回的记录数"),
):
    return {"skip": skip, "limit": limit}

# 需求:设计接口查询图书,要求携带两个查询参数:图书分类和价格
# 参数要求:图书分类:默认值为Python开发,长度5-255, 价格: 限制大小范围50-100
@app.get("/query/book")
async def get_query_book(
        kind: str = Query("Python",description="图书分类",min_length=5,max_length=255),
        price: int = Query(0,description="价格",ge=50,le=100)
):
    return {"类别": kind, "价格": price}

# 启动服务: uvicorn: Python中的轻量级Web服务器
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
