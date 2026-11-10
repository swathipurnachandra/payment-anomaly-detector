from redis_store.user_state import get_average_amount


AMOUNT_SPIKE_MULTIPLIER = 3


def check_amount_spike(transaction: dict) -> tuple[bool, str | None]:
    user_id = transaction["user_id"]
    amount = float(transaction["amount"])

    average_amount = get_average_amount(user_id)

    if amount > average_amount * AMOUNT_SPIKE_MULTIPLIER:
        return True, "Amount Spike"

    return False, None