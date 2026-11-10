from detector.amount_spike import check_amount_spike
from detector.location import check_impossible_travel
from detector.odd_hour import check_odd_hour
from detector.velocity import check_velocity


def detect(transaction: dict) -> dict:
    reasons = []

    velocity_anomaly, velocity_reason = check_velocity(transaction)
    if velocity_anomaly and velocity_reason:
        reasons.append(velocity_reason)

    amount_anomaly, amount_reason = check_amount_spike(transaction)
    if amount_anomaly and amount_reason:
        reasons.append(amount_reason)

    location_anomaly, location_reason = check_impossible_travel(transaction)
    if location_anomaly and location_reason:
        reasons.append(location_reason)

    odd_hour_anomaly, odd_hour_reason = check_odd_hour(transaction)
    if odd_hour_anomaly and odd_hour_reason:
        reasons.append(odd_hour_reason)

    return {
        "is_anomaly": bool(reasons),
        "reasons": reasons,
    }