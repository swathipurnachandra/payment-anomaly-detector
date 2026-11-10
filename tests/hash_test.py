from producer.users import users
from redis_store.redis_client import redis_client
from redis_store.user_state import create_user_state, get_user_state


def test_create_user_state():
    user = users[204]
    redis_client.delete(f"user:{user.user_id}")

    create_user_state(user)

    state = get_user_state(user.user_id)

    assert state["average_amount"] == str(user.average_amount)
    assert state["last_city"] == user.home_city
    assert state["transaction_count"] == "0"