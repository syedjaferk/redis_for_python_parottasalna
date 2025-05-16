import redis
import time
import uuid

class DistributedLock:
    def __init__(self, redis_client, lock_key, ttl=10):
        self.redis = redis_client
        self.lock_key = lock_key
        self.ttl = ttl  # lock expiration time in seconds
        self.lock_value = str(uuid.uuid4())

    def acquire(self):
        # SET key value NX EX ttl -> Set only if key does not exist (NX), and set expiry (EX)
        return self.redis.set(self.lock_key, self.lock_value, nx=True, ex=self.ttl)

    def release(self):
        # Use Lua script to release lock safely (check value before deleting)
        release_script = """
        if redis.call("get", KEYS[1]) == ARGV[1] then
            return redis.call("del", KEYS[1])
        else
            return 0
        end
        """
        return self.redis.eval(release_script, 1, self.lock_key, self.lock_value)

# Example Task
def process_task(task_id):
    lock_key = f"lock:task:{task_id}"
    redis_client = redis.Redis(host='localhost', port=6379, db=0)
    lock = DistributedLock(redis_client, lock_key, ttl=30)

    if lock.acquire():
        try:
            print(f"[{task_id}] Lock acquired. Processing task...")
            time.sleep(5)  # simulate processing
            print(f"[{task_id}] Task completed.")
        finally:
            lock.release()
            print(f"[{task_id}] Lock released.")
    else:
        print(f"[{task_id}] Task is already being processed elsewhere.")

# Sample usage
if __name__ == "__main__":
    process_task("abc123")
