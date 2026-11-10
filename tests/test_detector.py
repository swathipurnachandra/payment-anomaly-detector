from detector.detector import detect
from producer.users import users
from redis_store.redis_client import redis_client
from redis_store.user_state import create_user_state


def test_normal_transaction():
    user = users[2]
    redis_client.delete(f"velocity:{user.user_id}")
    create_user_state(user)

    transaction = {
        "user_id": user.user_id,
        "transaction_id": "normal-transaction",
        "event_time": 1_000_000,
        "amount": user.average_amount,
    }

    result = detect(transaction)

    assert result == {
        "is_anomaly": False,
        "reasons": [],
    }

def test_amount_spike_transaction():
    user = users[3]
    redis_client.delete(f"velocity:{user.user_id}")
    create_user_state(user)

    transaction = {
        "user_id": user.user_id,
        "transaction_id": "spike-transaction",
        "event_time": 1_000_001,
        "amount": user.average_amount * 4,
    }

    result = detect(transaction)

    assert result["is_anomaly"] is True
    assert "Amount Spike" in result["reasons"]