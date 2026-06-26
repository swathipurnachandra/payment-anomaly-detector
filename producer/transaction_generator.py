import random
import uuid
from datetime import datetime
from producer.merchants import MERCHANTS
from producer.locations import CITIES
from producer.anomalies import should_inject_anomaly
from producer.users import users

def generate_transaction():
    user = random.choice(users)

    amount = round(
        random.uniform(
            user["average_amount"] * 0.5,
            user["average_amount"] * 1.5
        ),
        2
    )

    transaction = {
        "transaction_id": str(uuid.uuid4()),

        "user_id": user["user_id"],

        "amount": amount,

        "merchant": random.choice(user["favorite_merchants"]),

        "city": user["home_city"],

        "payment_method": user["preferred_payment"],

        "timestamp": datetime.now().isoformat()
    }

    if should_inject_anomaly():
        transaction["is_anomaly"] = True
        transaction["anomaly_reason"] = "Amount Spike"
        transaction["amount"] = user["average_amount"] * random.randint(10, 25)

    return transaction