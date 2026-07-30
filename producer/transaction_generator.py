import random
import uuid
from datetime import datetime

from producer.anomalies import (
    inject_anomaly,
    should_inject_anomaly,
)

from producer.users import users

from shared.schemas import Transaction



def generate_transaction() -> Transaction:

    user = random.choice(users)
    now = datetime.now()
    timestamp = now.isoformat()
    event_time= int(now.timestamp())


    amount = round(
        random.uniform(
            user.average_amount * 0.5,
            user.average_amount * 1.5,
        ),
        2,
    )

    transaction = Transaction(
        transaction_id=str(uuid.uuid4()),
        user_id=user.user_id,
        amount=amount,
        merchant=random.choice(user.favorite_merchants),
        city=user.home_city,
        payment_method=user.preferred_payment,
        timestamp=timestamp,
        event_time=event_time,
        is_anomaly=False,
        anomaly_reason=None
    )

    if should_inject_anomaly():
        inject_anomaly(transaction, user)

    return transaction