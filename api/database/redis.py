import redis

redis_db =  redis.Redis(
    host= 'concept-cache', port='6379'
)


def get_redis_db():
    return redis_db

def set_dictionary_values():
    redis_db.hmset('status_names', {0: 'Inactive', 1: 'Active'})
    redis_db.expire('status_names', time=300)