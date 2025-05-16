
import os
import json
from pymongo.mongo_client import MongoClient

# Script to Find Data. 
def find_data(key):
    MONGO_CONN_STR = os.environ.get('MONGO_URI')
    mongo_client = MongoClient(MONGO_CONN_STR)
    database = mongo_client['test']
    collection = database["todos"]
    db_data = collection.find_one({'id': key}, {"_id": 0})
    print("DB Data ", db_data)
    return db_data

# Read Cache
def read_cache(event):
    key = event['key']
    print(key)
    data = execute('JSON.GET', key)
    if data:
        return data
    data = find_data(key)
    json_str = json.dumps(data)
    print(key, json_str)
    execute('JSON.SET', key, '.', json_str)
    override_reply(json_str)
    return json_str

GB('KeysReader').map(read_cache).register(commands=['JSON.GET'], mode='sync')
