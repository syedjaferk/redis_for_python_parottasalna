from redis_client import get_redis_client

STREAM_NAME = "event_stream"

def log_event(event_type, data):
    redis_client = get_redis_client()
    event = {
        "type": event_type,
        "data": data
    }
    event_id = redis_client.xadd(STREAM_NAME, event)
    print(f"Event logged with ID: {event_id}")

# Example
if __name__ == "__main__":
    log_event("user_signup", '{"user_id": 42, "email": "test@example.com"}')
    log_event("payment", '{"order_id": 123, "amount": 499.99}')
