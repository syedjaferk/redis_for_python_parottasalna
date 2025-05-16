import redis
import uuid
from datetime import datetime

r = redis.Redis(host='localhost', port=6379, db=0)

SESSION_TTL_SECONDS = 3600  # 1 hour sessions

def create_session(session_id, user_id, theme="light", language="en"):
    key = f"session:{session_id}"
    
    # Generate a unique access token
    access_token = str(uuid.uuid4())
    
    session_data = {
        "user_id": user_id,
        "login_time": datetime.utcnow().isoformat(),
        "last_activity": datetime.utcnow().isoformat(),
        "theme": theme,
        "language": language,
        "access_token": access_token
    }
    r.hset(key, mapping=session_data)
    r.expire(key, SESSION_TTL_SECONDS)
    print(f"Session {session_id} created with TTL {SESSION_TTL_SECONDS}s and access token {access_token}.")
    return access_token

def update_session_activity(session_id):
    key = f"session:{session_id}"
    if r.exists(key):
        r.hset(key, "last_activity", datetime.utcnow().isoformat())
        r.expire(key, SESSION_TTL_SECONDS)  # Reset TTL on activity
        print(f"Session {session_id} activity updated.")
    else:
        print(f"Session {session_id} not found or expired.")

def get_session(session_id):
    key = f"session:{session_id}"
    if not r.exists(key):
        print(f"Session {session_id} not found or expired.")
        return None
    data = r.hgetall(key)
    return {k.decode(): v.decode() for k, v in data.items()}

def delete_session(session_id):
    key = f"session:{session_id}"
    r.delete(key)
    print(f"Session {session_id} deleted.")

# Example usage

access_token = create_session("sess123", "user1001", theme="dark", language="fr")
print(get_session("sess123"))

update_session_activity("sess123")
print(get_session("sess123"))

delete_session("sess123")
print(get_session("sess123"))
