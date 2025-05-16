from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import redis
import uuid
import json

app = FastAPI()
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Task Model
class Task(BaseModel):
    title: str
    description: str
    assigned_to: str

# Create Task
@app.post("/task")
def create_task(task: Task):
    task_id = str(uuid.uuid4())
    task_data = task.dict()
    task_data['id'] = task_id
    r.hset(f"task:{task_id}", mapping=task_data)
    r.rpush("task_queue", task_id)  # Add to queue
    r.publish("tasks", json.dumps(task_data))  # Pub/Sub
    return {"msg": "Task created", "id": task_id}

# Get Task
@app.get("/task/{task_id}")
def get_task(task_id: str):
    task = r.hgetall(f"task:{task_id}")
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# Task Leaderboard
@app.post("/contribute/{user_id}")
def update_leaderboard(user_id: str):
    r.zincrby("leaderboard", 1, user_id)
    return {"msg": "Contribution recorded"}

@app.get("/leaderboard")
def get_leaderboard():
    top_users = r.zrevrange("leaderboard", 0, 9, withscores=True)
    return {"top_users": top_users}

# API Rate Limiting
@app.get("/limited")
def limited_endpoint(user_id: str):
    key = f"rate:{user_id}"
    current = r.get(key)
    if current and int(current) >= 5:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    pipe = r.pipeline()
    pipe.incr(key, 1)
    pipe.expire(key, 60)  # 60 seconds window
    pipe.execute()
    return {"msg": "Allowed"}

