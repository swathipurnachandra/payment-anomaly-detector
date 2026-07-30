from detector.velocity import check_velocity
from redis_store.user_state import (
    create_user_state,
    increment_transaction_count,
)
from producer.users import users

user = users[0]

create_user_state(user)

for _ in range(6):
    increment_transaction_count(user.user_id)

print(check_velocity(user.user_id))