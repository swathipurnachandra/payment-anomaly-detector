from detector.amount_spike import check_amount_spike
from producer.users import users
from redis_store.redis_client import redis_client
from redis_store.user_state import create_user_state


def test_amount_below_spike_threshold():
    user = users[0]
    create_user_state(user)

    transaction = {
        "user_id": user.user_id,
        "amount": user.average_amount * 2,
    }

    assert check_amount_spike(transaction) == (False, None)


def test_amount_above_spike_threshold():
    user = users[1]
    create_user_state(user)

    transaction = {
        "user_id": user.user_id,
        "amount": user.average_amount * 4,
    }

    assert check_amount_spike(transaction) == (True, "Amount Spike")