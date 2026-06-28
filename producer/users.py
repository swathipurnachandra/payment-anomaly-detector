import random

from shared.constants import (
    CITIES,
    MERCHANTS,
    PAYMENT_METHODS,
)

from shared.schemas import UserProfile

users: list[UserProfile] = []

for user_id in range(1, 1001):

    users.append(
        UserProfile(
            user_id=user_id,
            home_city=random.choice(CITIES),
            preferred_payment=random.choice(PAYMENT_METHODS),
            average_amount=random.randint(300, 5000),
            favorite_merchants=random.sample(MERCHANTS, 3),
        )
    )