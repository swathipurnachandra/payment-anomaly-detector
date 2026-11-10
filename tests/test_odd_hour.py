from detector.odd_hour import check_odd_hour
from producer.users import users
from redis_store.redis_client import redis_client
from redis_store.user_state import create_user_state


def test_odd_hour_high_value_transaction_is_flagged():
    user = users[0]
    redis_client.delete(f"user:{user.user_id}")
    create_user_state(user)

    transaction = {
        "user_id": user.user_id,
        "amount": user.average_amount * 4,
        "timestamp": "2026-06-10T03:17:42",
    }

    assert check_odd_hour(transaction) == (True, "Odd Hour")


def test_odd_hour_low_value_transaction_is_not_flagged():
    user = users[1]
    redis_client.delete(f"user:{user.user_id}")
    create_user_state(user)

    transaction = {
        "user_id": user.user_id,
        "amount": user.average_amount * 1.5,
        "timestamp": "2026-06-10T04:00:00",
    }

    assert check_odd_hour(transaction) == (False, None)
