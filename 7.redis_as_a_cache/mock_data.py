from pymongo.mongo_client import MongoClient
from faker import Faker  

fake = Faker()  

# Mongo Db Connection
MONGO_CONN_STR = "mongodb://localhost:27017"
mongo_client = MongoClient(MONGO_CONN_STR)
database = mongo_client['test']
collection = database["todos"]

for itr in range(1, 1000000):
    data = {
        "id": str(itr),
        "name": fake.name(),
        "description": fake.text(100)
    }
    collection.insert_one(data)
    print(data)


