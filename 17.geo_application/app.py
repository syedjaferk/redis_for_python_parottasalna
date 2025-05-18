# main.py
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import redis
from typing import List
import time
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

r = redis.Redis(host="localhost", port=6379, decode_responses=True)
GEO_KEY = "captains"

@app.post("/update_location/")
def update_location(captain_id: str, lat: float, lon: float):
    r.geoadd(GEO_KEY, (lon, lat, captain_id))
    r.set(f"ttl:{captain_id}", time.time(), ex=15)
    return {"status": "updated"}

@app.get("/nearby_captains/")
def nearby_captains(lat: float, lon: float, radius: int = 100):
    all_ids = r.zrange(GEO_KEY, 0, -1)
    valid_ids = [cid for cid in all_ids if r.exists(f"ttl:{cid}")]

    temp_key = "temp:valid_captains"
    r.delete(temp_key)
    for cid in valid_ids:
        pos = r.geopos(GEO_KEY, cid)[0]
        if pos:
            r.geoadd(temp_key, (pos[0], pos[1], cid))

    result = r.geosearch(temp_key, longitude=lon, latitude=lat, radius=radius / 1000, unit="km")
    captains = [{"id": cid, "pos": r.geopos(GEO_KEY, cid)[0]} for cid in result]
    r.delete(temp_key)
    return {"captains": captains}

@app.post("/simulate_captains/")
def simulate_captains(count: int = 100):
    base_lat, base_lon = 13.0827, 80.2707
    for i in range(count):
        lat = base_lat + random.uniform(-0.01, 0.01)
        lon = base_lon + random.uniform(-0.01, 0.01)
        captain_id = f"captain_{i}"
        r.geoadd(GEO_KEY, (lon, lat, captain_id))
        r.set(f"ttl:{captain_id}", time.time(), ex=60)
    return {"status": "populated"}
