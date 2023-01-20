from fastapi import Depends
import redis
from settings import Settings

settings = Settings()

redis_db =  redis.Redis(
    host= settings.redis_host, port=settings.redis_port
)


def get_redis_db():
    return redis_db
