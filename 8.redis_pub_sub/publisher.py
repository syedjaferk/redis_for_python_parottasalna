import redis
import time

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

messages = [
    "New comment on your post!",
    "You have 2 new followers.",
    "System maintenance at 12AM.",
]

for msg in messages:
    r.publish('notifications', msg)
    print(f"✅ Sent: {msg}")
    time.sleep(2)
