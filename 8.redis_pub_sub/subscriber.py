import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)
pubsub = r.pubsub()
pubsub.subscribe('notifications')

print("Subscribed to 'notifications' channel...")

for message in pubsub.listen():
    if message['type'] == 'message':
        print(f"📨 New Notification: {message['data']}")
