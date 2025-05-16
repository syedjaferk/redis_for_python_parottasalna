import redis
from datetime import datetime

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

def track_visit(user_id):
    today = datetime.utcnow().strftime("%Y-%m-%d")
    key = f"visitors:{today}"
    r.pfadd(key, user_id)

def get_unique_visitors(date_str):
    key = f"visitors:{date_str}"
    return r.pfcount(key)

# Simulating visits
track_visit("user1")
track_visit("user2")
track_visit("user3")
track_visit("user1")  # duplicate

print("Unique visitors today:", get_unique_visitors(datetime.utcnow().strftime("%Y-%m-%d")))

