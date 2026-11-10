import uuid
from time import time

from detector.velocity import check_velocity
from redis_store.redis_client import redis_client


USER_ID = 999


def test_velocity_flags_six_transactions_in_one_window():
    redis_client.delete(f"velocity:{USER_ID}")
    event_time = int(time())
    results = []

    for _ in range(6):
        transaction = {
            "user_id": USER_ID,
            "transaction_id": str(uuid.uuid4()),
            "event_time": event_time,
        }

        results.append(check_velocity(transaction))

    assert results == [
        (False, None),
        (False, None),
        (False, None),
        (False, None),
        (False, None),
        (True, "Velocity"),
    ]