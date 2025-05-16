from redis_client import get_redis_client
import time

STREAM_NAME = "event_stream"
GROUP_NAME = "event_consumers"
CONSUMER_NAME = "consumer_1"

def init_group():
    redis_client = get_redis_client()
    try:
        redis_client.xgroup_create(STREAM_NAME, GROUP_NAME, id='0', mkstream=True)
        print("Consumer group created.")
    except redis.exceptions.ResponseError as e:
        if "BUSYGROUP" in str(e):
            print("Consumer group already exists.")
        else:
            raise

def consume_events():
    redis_client = get_redis_client()
    print("Waiting for events...")
    while True:
        events = redis_client.xreadgroup(
            groupname=GROUP_NAME,
            consumername=CONSUMER_NAME,
            streams={STREAM_NAME: '>'},
            count=5,
            block=2000  # milliseconds
        )

        for stream_name, messages in events:
            for message_id, message_data in messages:
                print(f"Processing event {message_id}: {message_data}")
                # Simulate processing
                time.sleep(1)
                redis_client.xack(STREAM_NAME, GROUP_NAME, message_id)

if __name__ == "__main__":
    init_group()
    consume_events()
