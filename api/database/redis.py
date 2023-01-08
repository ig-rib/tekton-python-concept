from redis_om import get_redis_connection
    
redis_db = get_redis_connection(
    host= 'concept-cache', port='6739'
    )

redis_db.set('hi', 'hi')
print(redis_db.get('hi'))