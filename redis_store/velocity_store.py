from redis_store.redis_client import redis_client

WINDOW_SIZE = 60
VELOCITY_THRESHOLD = 5


def add_transaction(user_id: int, transaction_id: str, event_time: int):
    key = f"velocity:{user_id}"

    redis_client.zadd(
        key,
        {
            transaction_id: event_time
        }
    )


def remove_old_transactions(user_id: int, current_time: int):
    key = f"velocity:{user_id}"

    redis_client.zremrangebyscore(
        key,
        0,
        current_time - WINDOW_SIZE
    )


def get_recent_transaction_count(user_id: int):
    key = f"velocity:{user_id}"

    return redis_client.zcard(key)