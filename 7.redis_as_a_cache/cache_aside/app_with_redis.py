from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo.mongo_client import MongoClient
import redis


r = redis.Redis(host='localhost', port=6379, decode_responses=True)
app = FastAPI()

# Mongo Db Connection
MONGO_CONN_STR = "mongodb://localhost:27017"
mongo_client = MongoClient(MONGO_CONN_STR)
database = mongo_client['test']
collection = database["todos"]

class Todo(BaseModel):
    id: str
    name: str
    description: str = None

@app.post("/todos/")
def create_todo(todo: Todo):
    collection.insert_one(todo.dict())
    return {} 

@app.get("/todos/{todo_id}", response_model=Todo)
def read_item(todo_id: str):
    from_cache = r.hgetall(todo_id)
    if from_cache:
        return from_cache
    todo = collection.find_one({"id": todo_id}, {'_id':0})
    r.hmset(todo_id, todo)
    if todo:
        return todo
    raise HTTPException(status_code=404, detail="Item not found")