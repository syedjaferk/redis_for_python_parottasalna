import redis

r = redis.Redis()
chat_key = "chat:room1"

def post_message(user, message):
    text = f"{user}: {message}"
    r.rpush(chat_key, text)
    r.ltrim(chat_key, -100, -1)  # Keep only last 100 messages
    print(f"Message sent: {text}")

def get_recent_messages():
    messages = r.lrange(chat_key, 0, -1)
    return [m.decode() for m in messages]

# Demo usage
post_message("jafer", "Hello room!")
post_message("alice", "Hi everyone!")

print("Recent messages:")
for msg in get_recent_messages():
    print(msg)
