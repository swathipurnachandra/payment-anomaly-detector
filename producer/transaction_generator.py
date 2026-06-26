import random
import datetime
import uuid
from producer.merchants import MERCHANTS
from producer.locations import CITIES
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

    return transaction