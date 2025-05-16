import redis
import time

r = redis.Redis(host='localhost', port=6379, db=0)

# Sample jobs to enqueue
jobs = [
    "send_email:user1@example.com",
    "resize_image:img123.jpg",
    "generate_invoice:order567"
]

for job in jobs:
    r.lpush("task_queue", job)
    print(f"[Producer] Job added: {job}")
    time.sleep(1)  # simulate delay


import redis
import time

r = redis.Redis(host='localhost', port=6379, db=0)

print("[Consumer] Waiting for jobs...")

while True:
    job = r.brpop("task_queue", timeout=0)  # blocking pop
    if job:
        queue_name, job_data = job
        print(f"[Consumer] Processing job: {job_data.decode()}")
        time.sleep(2)  # simulate processing