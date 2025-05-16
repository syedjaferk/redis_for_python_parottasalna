# What is this ?

An implementation of different types of Caches using Redis, MongoDb & FastApi.
    1. Cache Aside
    2. Read Through
    3. Write Through
    4. Write Behind

# How to set up ?


## Redis:

```
    docker run -p 6379:6379 --rm redislabs/redismod:latest
```

## MongoDb:

```
docker run --name mongo_container -p 27017:27017 --rm mongo
```
We have a backup of 2 Lakhs data. To Restore data to mongo db, 

```
docker exec -i mongo_container sh -c 'mongorestore --archive' < 2l_data.dump
```

> Note: For benchmarking, we are using locust to see the performance attained after using cache. 