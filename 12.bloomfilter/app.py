from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
import redis

# ---------- Redis Setup ----------
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
bloom_key = "username:bloomfilter"
try:
    redis_client.execute_command('BF.RESERVE', bloom_key, 0.01, 100000)
except redis.exceptions.ResponseError:
    pass  # already exists

# ---------- MongoDB Setup ----------
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client['userdb']
user_collection = db['users']

# ---------- FastAPI Setup ----------
app = FastAPI()

class User(BaseModel):
    username: str

@app.post("/register")
def register(user: User):
    username = user.username.lower()

    # Bloom check
    might_exist = redis_client.execute_command('BF.EXISTS', bloom_key, username)
    if might_exist:
        # Confirm with MongoDB
        if user_collection.find_one({"username": username}):
            raise HTTPException(status_code=400, detail="Username already taken")

    # Save to MongoDB
    user_collection.insert_one({"username": username})

    # Add to Bloom Filter
    redis_client.execute_command('BF.ADD', bloom_key, username)

    return {"message": f"User '{username}' registered successfully"}

@app.get("/check/{username}")
def check_username(username: str):
    username = username.lower()
    might_exist = redis_client.execute_command('BF.EXISTS', bloom_key, username)

    if not might_exist:
        return {"available": True, "checked": "redis"}

    # Confirm with MongoDB
    exists = user_collection.find_one({"username": username}) is not None
    return {"available": not exists, "checked": "mongo"}
