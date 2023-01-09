import redis
from settings import Settings

settings = Settings()

redis_db =  redis.Redis(
    host= settings.redis_host, port=settings.redis_port
)


def get_redis_db():
    return redis_db

def set_dictionary_values():
    redis_db.hmset('status_names', {0: 'Inactive', 1: 'Active'})
    redis_db.expire('status_names', time=300)