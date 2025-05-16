import redis

r = redis.Redis(host='localhost', port=6379, db=0)

# 1. Create or update hash fields
r.hset("user:1000", mapping={"name": "Alice", "age": "30", "city": "Paris"})

# 2. Get a single field
name = r.hget("user:1000", "name")
print("Name:", name.decode())  # Output: Alice

# 3. Get all fields and values
user_data = r.hgetall("user:1000")
user_data_decoded = {k.decode(): v.decode() for k, v in user_data.items()}
print("User Data:", user_data_decoded)
# Output: {'name': 'Alice', 'age': '30', 'city': 'Paris'}

# 4. Check if a field exists
exists = r.hexists("user:1000", "age")
print("Age field exists?", bool(exists))  # Output: True

# 5. Delete a field
r.hdel("user:1000", "city")

# 6. Increment a numeric field
r.hincrby("user:1000", "age", 1)
new_age = r.hget("user:1000", "age").decode()
print("New Age:", new_age)  # Output: 31
