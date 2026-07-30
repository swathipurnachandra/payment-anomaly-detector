import time
import uuid

from detector.velocity import check_velocity

user_id = 999

for i in range(6):
    transaction = {
        "user_id": user_id,
        "transaction_id": str(uuid.uuid4()),
        "event_time": int(time.time())
    }

    print(check_velocity(transaction))