import redis
import logging
from redis.exceptions import ConnectionError, TimeoutError, AuthenticationError, RedisError
from config.config import REDIS_DB, REDIS_HOST, REDIS_PASSWORD, REDIS_PORT


class RedisFallback:
    """A fallback class that mimics Redis client but returns None for all operations."""

    def __init__(self, error_message="Redis connection failed"):
        self.error_message = error_message
        logging.error(error_message)

    def get(self, *args, **kwargs):
        logging.warning(f"Redis get operation failed: {self.error_message}")
        return None

    def set(self, *args, **kwargs):
        logging.warning(f"Redis set operation failed: {self.error_message}")
        return None

    def delete(self, *args, **kwargs):
        logging.warning(f"Redis delete operation failed: {self.error_message}")
        return None

    def __getattr__(self, name):
        def method(*args, **kwargs):
            logging.warning(f"Redis {name} operation failed: {self.error_message}")
            return None
        return method


def get_redis_api_db():
    try:
        return redis.Redis(
            host=REDIS_HOST,
            db=REDIS_DB,
            port=REDIS_PORT,
            password=REDIS_PASSWORD,
            decode_responses=True
        )
    except (ConnectionError, TimeoutError, AuthenticationError, RedisError) as e:
        error_message = f"Failed to connect to Redis: {e}"
        return RedisFallback(error_message)


try:
    r = get_redis_api_db()
except Exception as e:
    error_message = f"Unexpected error initializing Redis connection: {e}"
    r = RedisFallback(error_message)
