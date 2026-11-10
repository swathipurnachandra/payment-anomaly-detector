from shared.constants import ODD_HOUR_START, ODD_HOUR_END, HIGH_VALUE_MULTIPLIER
from redis_store.user_state import get_average_amount


def check_odd_hour(transaction: dict) -> tuple[bool, str | None]:
    amount = float(transaction["amount"])
    user_id = transaction["user_id"]

    # Convert ISO timestamp into datetime
    from datetime import datetime

    timestamp = transaction["timestamp"]
    dt = datetime.fromisoformat(timestamp)

    hour = dt.hour

    # Example: odd hour means between midnight and 5 AM
    if hour < ODD_HOUR_START or hour >= ODD_HOUR_END:
        return False, None

    average_amount = get_average_amount(user_id)

    if amount > average_amount * HIGH_VALUE_MULTIPLIER:
        return True, "Odd Hour"

    return False, None