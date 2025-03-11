import redis

def get_redis_api_db():
    return redis.Redis(
        host='localhost',
        db=0,
        port=16379,
        password="Us5EfbrcBW",
        decode_responses=True
    )

r = get_redis_api_db()
print(r.get('foo'))