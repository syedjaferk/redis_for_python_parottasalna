import redis
import json

# Create Redis client with JSON support
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Create JSON document
user_profile = {
    "name": "Alice",
    "email": "alice@example.com",
    "age": 28,
    "preferences": {
        "theme": "dark",
        "language": "en"
    }
}

# Set JSON
r.json().set("user:1001", "$", user_profile)

# Get full document
print("Full user:", r.json().get("user:1001"))

# Get specific field
print("Name:", r.json().get("user:1001", "$.name"))

# Update age
r.json().set("user:1001", "$.age", 29)

# Increment age
r.json().numincrby("user:1001", "$.age", 1)

# Delete a field
r.json().delete("user:1001", "$.preferences.language")

# Delete entire document
r.json().delete("user:1001")
