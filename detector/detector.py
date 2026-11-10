from detector.amount_spike import check_amount_spike
from detector.velocity import check_velocity


def detect(transaction: dict) -> dict:
    reasons = []

    velocity_anomaly, velocity_reason = check_velocity(transaction)

    if velocity_anomaly and velocity_reason:
        reasons.append(velocity_reason)

    amount_anomaly, amount_reason = check_amount_spike(transaction)

    if amount_anomaly and amount_reason:
        reasons.append(amount_reason)

    return {
        "is_anomaly": bool(reasons),
        "reasons": reasons,
    }