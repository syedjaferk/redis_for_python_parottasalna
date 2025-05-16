import redis
from datetime import datetime, timedelta
import random
import time

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# --- CONFIG ---
HLL_TTL_SECONDS = 3600  # expire each HLL key after 1 hour

# Simulate user visits
def track_visit(user_id: str):
    now_minute = datetime.utcnow().strftime("%Y-%m-%dT%H:%M")
    hll_key = f"hll:visitors:{now_minute}"

    # Add user to HLL and expire key later
    r.pfadd(hll_key, user_id)
    r.expire(hll_key, HLL_TTL_SECONDS)

    print(f"[{now_minute}] Tracked visit: {user_id}")

# Estimate number of unique visitors in the last N minutes
def get_unique_visitors_last_n_minutes(n: int = 5):
    now = datetime.utcnow()
    keys = [
        f"hll:visitors:{(now - timedelta(minutes=i)).strftime('%Y-%m-%dT%H:%M')}"
        for i in range(n)
    ]

    # Merge into a temporary key
    temp_key = "hll:temp:merged"
    r.pfmerge(temp_key, *keys)

    # Optional: Set a short TTL on the temp key to avoid clutter
    r.expire(temp_key, 60)

    return r.pfcount(temp_key)

# Simulate incoming traffic
def simulate_traffic():
    for _ in range(100):  # simulate 100 user visits
        user_id = f"user_{random.randint(1, 50)}"  # some repeat users
        track_visit(user_id)
        time.sleep(0.5)  # simulate half-second between visits

# Main
if __name__ == "__main__":
    simulate_traffic()

    print("\n--- Estimating Unique Users ---")
    estimated = get_unique_visitors_last_n_minutes(5)
    print(f"Estimated unique users in last 5 minutes: {estimated}")
