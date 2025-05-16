import redis
import time

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

# Set key with expiration
r.set("otp:123456", "user_id_1001", ex=300)  # 5 minutes
print("OTP stored.")

# Set expiration after setting key
r.set("tempkey", "some value")
r.expire("tempkey", 10)
print("tempkey will expire in 10 seconds.")

# Check TTL
ttl = r.ttl("tempkey")
print(f"TTL for tempkey: {ttl} seconds")

# Wait and test expiration
time.sleep(11)
val = r.get("tempkey")
print("Value after expiration:", val)  # Should be None
