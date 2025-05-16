# Cache Aside

Application checks whether the data is present in the cache (In our case redis). If data is present it returns the data. Else checks from the database and stores it in Cache and then returns the data to client.


# When to use

1. If you have a static data. 
2. It contains only the data which is actually needed. So its cost effective. 
3. Unpredictable resource demand. 


# When not to use

1. Highly Dynamic data. Since cache is stored only after a cache miss; this is costly. 
2. Not good for storing session state in web application. 


# How to run ?

1. Start redis

```
docker run -p 6379:6379 --rm redislabs/redismod:latest
```

2. Start MongoDb

```
docker run -p 27017:27017 --name mongo_container --rm mongo
```
We have a backup of 2 Lakhs data. To Restore data to mongo db, 

```
docker exec -i mongo_container sh -c 'mongorestore --archive' < 2l_data.dump
```

3. Start Flask Application

```
uvicorn app:app --port 8000
```

4. Run Locust

```
locust -f locust_file.py -t 1m -u 100 -r 100
```

5. Start Flask application with redis, 

```
uvicorn app_with_redis:app --port 8000
```

6. Run Locust

```
locust -f locust_file.py -t 1m -u 100 -r 100
```



# References

1. https://learn.microsoft.com/en-us/azure/architecture/patterns/cache-aside
2. https://docs.aws.amazon.com/whitepapers/latest/database-caching-strategies-using-redis/caching-patterns.html