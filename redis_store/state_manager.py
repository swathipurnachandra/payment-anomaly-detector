from producer.users import users

from redis_store.user_state import (
    create_user_state,
    get_user_state,
    increment_transaction_count,
    update_last_city,
    update_last_seen,
    user_exists,
)


def ensure_user_state(user_id: int) -> None:
    if user_exists(user_id):
        return

    user = next(
        (user for user in users if user.user_id == user_id),
        None,
    )
    if user is None:
        raise ValueError(f"Unknown user ID: {user_id}")

    create_user_state(user)


def process_transaction(transaction):
    user_id = transaction["user_id"]

    ensure_user_state(user_id)

    increment_transaction_count(user_id)

    update_last_city(
        user_id,
        transaction["city"],
    )

    update_last_seen(
        user_id,
        transaction["timestamp"],
    )

    return get_user_state(user_id)