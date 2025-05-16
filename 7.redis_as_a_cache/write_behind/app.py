from rgsync import RGJSONWriteBehind, RGJSONWriteThrough
from rgsync.Connectors import MongoConnector, MongoConnection

import os
mongoUrl = os.environ.get('MONGO_URI')
connection = MongoConnection("", "", "", "", mongoUrl)

db = "test"
collection = "todos"

movieConnector = MongoConnector(connection, db, collection, 'id')
RGJSONWriteBehind(GB, keysPrefix='todos',
connector=movieConnector, name='TodoWriteBehind',
version='99.99.99')