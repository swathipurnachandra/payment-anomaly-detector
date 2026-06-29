from shared.schemas import UserProfile
from redis_store.redis_client import redis_client


def get_key(user_id: int) -> str:
    return f"user:{user_id}"


def create_user_state(user: UserProfile):

    key = get_key(user.user_id)

    redis_client.hset(
        key,
        mapping={
            "average_amount": user.average_amount,
            "last_city": user.home_city,
            "transaction_count": 0,
            "last_seen": "",
        },
    )


def user_exists(user_id: int):

    return redis_client.exists(get_key(user_id))


def increment_transaction_count(user_id: int):

    redis_client.hincrby(
        get_key(user_id),
        "transaction_count",
        1,
    )


def update_last_city(user_id: int, city: str):

    redis_client.hset(
        get_key(user_id),
        "last_city",
        city,
    )


def update_last_seen(user_id: int, timestamp: str):

    redis_client.hset(
        get_key(user_id),
        "last_seen",
        timestamp,
    )


def get_user_state(user_id: int):

    return redis_client.hgetall(get_key(user_id))