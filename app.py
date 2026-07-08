from fastapi import FastAPI
import redis
import os

app = FastAPI()

# Connect to Redis container over the Docker Compose network
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=6379,
    decode_responses=True
)


@app.get("/")
def root():
    return {"message": "FastAPI + Redis is running"}


@app.post("/hit/{key}")
def hit(key: str):
    count = redis_client.incr(key)
    return {
        "key": key,
        "count": count
    }


@app.get("/count/{key}")
def count(key: str):
    value = redis_client.get(key)

    if value is None:
        value = 0

    return {
        "key": key,
        "count": int(value)
    }


@app.get("/healthz")
def health():
    try:
        redis_client.ping()
        return {
            "status": "ok",
            "redis": "up"
        }
    except Exception:
        return {
            "status": "error",
            "redis": "down"
        }
