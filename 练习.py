from fastapi import FastAPI
from pydantic import BaseModel,Field
app = FastAPI()
@app.get("/")
async def root():
    return {"message": "Hello World"}


class Task(BaseModel):
    task_name: str =Field(...,min_length=2,max_length=30)
    priority: int = Field(default=3,ge=1,le=5)
    enabled: bool = Field(default=True)
@app.post("/tasks")
async def create_task(task: Task):
    return task