from detector.velocity import check_velocity


def detect(transaction):
    """
    Runs all fraud detection rules.
    """

    is_anomaly, reason = check_velocity(transaction["user_id"])

    return {
        "is_anomaly": is_anomaly,
        "reason": reason,
    }