import random
from producer.locations import CITIES
from producer.merchants import MERCHANTS

PAYMENT_METHODS = [
    "UPI",
    "Credit Card",
    "Debit Card",
    "Wallet",
    "Net Banking"
]

users = []

for user_id in range(1, 1001):

    users.append({
        "user_id": user_id,

        "home_city": random.choice(CITIES),

        "preferred_payment": random.choice(PAYMENT_METHODS),

        "average_amount": random.randint(300, 5000),

        "favorite_merchants": random.sample(MERCHANTS, 3)
    })