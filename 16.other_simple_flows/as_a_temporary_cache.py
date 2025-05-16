import time
import redis
import json
from random import randint

# Connect to local Redis server
r = redis.Redis(host='localhost', port=6379, db=0)

CACHE_KEY = "exchange_rates"
CACHE_TTL = 30  # seconds

def fetch_exchange_rates_from_source():
    """Simulate an expensive API call to get exchange rates"""
    print("Fetching from external source...")
    time.sleep(2)  # simulate delay
    # Simulated data
    return {
        "USD": randint(70, 75),
        "EUR": randint(80, 85),
        "JPY": randint(0, 2)
    }

def get_exchange_rates():
    cached_data = r.get(CACHE_KEY)
    
    if cached_data:
        print("Fetched from Redis cache.")
        return json.loads(cached_data)
    
    # If not in cache, fetch from source and store in Redis
    data = fetch_exchange_rates_from_source()
    r.set(CACHE_KEY, json.dumps(data), ex=CACHE_TTL)
    print("Stored data in Redis.")
    return data

if __name__ == "__main__":
    rates = get_exchange_rates()
    print("Exchange Rates:", rates)
