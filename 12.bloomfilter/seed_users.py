from faker import Faker
from pymongo import MongoClient
from tqdm import tqdm

# MongoDB setup
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client['userdb']
user_collection = db['users']

# Faker setup
fake = Faker()
Faker.seed(0)

# Number of users to generate
N = 10_000

# Clear old data
user_collection.delete_many({})

# Generate and insert fake users
users = []
for _ in tqdm(range(N), desc="Generating Users"):
    username = fake.unique.user_name().lower()
    users.append({"username": username})

# Bulk insert
user_collection.insert_many(users)
print(f"✅ Inserted {N} users into MongoDB.")
