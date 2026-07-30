from redis_store.velocity_store import (
    add_transaction,
    remove_old_transactions,
    get_recent_transaction_count,
)

VELOCITY_THRESHOLD = 5


def check_velocity(transaction):
    """
    Returns:
        (is_anomaly, reason)
    """

    user_id = transaction["user_id"]
    transaction_id = transaction["transaction_id"]
    event_time = transaction["event_time"]

    #Store this transaction
    add_transaction(user_id, transaction_id, event_time)

    #Remove transactions older than 60 seconds
    remove_old_transactions(user_id, event_time)

    #Count remaining transactions
    count = get_recent_transaction_count(user_id)

    #Decide
    if count > VELOCITY_THRESHOLD:
        return True, "Velocity"

    return False, None