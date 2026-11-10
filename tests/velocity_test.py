import time
import uuid

from detector.velocity import check_velocity
from redis_store.redis_client import redis_client


USER_ID = 999


redis_client.delete(f"velocity:{USER_ID}")

for _ in range(6):
    transaction = {
        "user_id": USER_ID,
        "transaction_id": str(uuid.uuid4()),
        "event_time": int(time.time()),
    }

    print(check_velocity(transaction))