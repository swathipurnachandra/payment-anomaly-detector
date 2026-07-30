from redis_store.user_state import get_user_state


VELOCITY_THRESHOLD = 5


def check_velocity(user_id: int):
    """
    Returns:
        (is_anomaly, reason)
    """

    state = get_user_state(user_id)

    count = int(state["transaction_count"])

    if count > VELOCITY_THRESHOLD:
        return True, "Velocity"

    return False, None