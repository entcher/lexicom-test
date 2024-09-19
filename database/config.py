import redis.asyncio as redis


class RedisClient:
    pool: redis.ConnectionPool = None

    @classmethod
    def init(cls, host: str = 'redis', port: int = 6379):
        try:
            cls.pool = redis.ConnectionPool(host=host, port=port)
        except redis.RedisError as e:
            print(f'Error while creating {e}')

    @classmethod
    def get_redis(cls):
        return redis.Redis(connection_pool=cls.pool)
