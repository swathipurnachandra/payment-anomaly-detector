import random
from datetime import datetime

from shared.constants import (
    ANOMALY_TYPES,
    CITIES,
    PAYMENT_METHODS,
    UNKNOWN_MERCHANT,
)


def should_inject_anomaly(probability=0.03):
    return random.random() < probability


def inject_anomaly(transaction, user):

    anomaly = random.choice(ANOMALY_TYPES)

    transaction.is_anomaly = True
    transaction.anomaly_reason = anomaly

    if anomaly == "Amount Spike":
        transaction.amount = (
            user.average_amount * random.randint(10, 25)
        )

    elif anomaly == "Location Change":

        other_cities = [
            city
            for city in CITIES
            if city != user.home_city
        ]

        transaction.city = random.choice(other_cities)

    elif anomaly == "Payment Method Change":

        other_methods = [
            method
            for method in PAYMENT_METHODS
            if method != user.preferred_payment
        ]

        transaction.payment_method = random.choice(other_methods)

    elif anomaly == "Unknown Merchant":

        transaction.merchant = UNKNOWN_MERCHANT

    elif anomaly == "Odd Hour Transaction":
        dt = datetime.fromisoformat(transaction.timestamp)
        dt = dt.replace(hour=3, minute=17, second=42, microsecond=0)

        transaction.timestamp = dt.isoformat()
        transaction.event_time = int(dt.timestamp())

    return transaction