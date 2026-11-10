import uuid
from time import time

from detector.velocity import check_velocity
from redis_store.redis_client import redis_client


USER_ID = 998


def test_velocity_ignores_transactions_outside_window():
    redis_client.delete(f"velocity:{USER_ID}")
    current_time = int(time())

    check_velocity(
        {
            "user_id": USER_ID,
            "transaction_id": str(uuid.uuid4()),
            "event_time": current_time - 61,
        }
    )

    for _ in range(5):
        result = check_velocity(
            {
                "user_id": USER_ID,
                "transaction_id": str(uuid.uuid4()),
                "event_time": current_time,
            }
        )

    assert result == (False, None)