from datetime import datetime, timezone

from detector.location import check_impossible_travel
from producer.users import users
from redis_store.redis_client import redis_client
from redis_store.user_state import create_user_state


def test_impossible_travel_is_detected():
    user = users[0]
    redis_client.delete(f"user:{user.user_id}")
    create_user_state(user)

    previous_time = datetime(2026, 1, 1, tzinfo=timezone.utc)
    redis_client.hset(
        f"user:{user.user_id}",
        mapping={
            "last_city": "Chennai",
            "last_seen": previous_time.isoformat(),
            "transaction_count": 1,
        },
    )

    transaction = {
        "user_id": user.user_id,
        "city": "Delhi",
        "event_time": int(previous_time.timestamp()) + 3600,
    }

    assert check_impossible_travel(transaction) == (
        True,
        "Impossible Travel",
    )


def test_same_city_is_not_impossible_travel():
    user = users[1]
    redis_client.delete(f"user:{user.user_id}")
    create_user_state(user)

    previous_time = datetime(2026, 1, 1, tzinfo=timezone.utc)
    redis_client.hset(
        f"user:{user.user_id}",
        mapping={
            "last_city": "Chennai",
            "last_seen": previous_time.isoformat(),
        },
    )

    transaction = {
        "user_id": user.user_id,
        "city": "Chennai",
        "event_time": int(previous_time.timestamp()) + 60,
    }

    assert check_impossible_travel(transaction) == (False, None)
