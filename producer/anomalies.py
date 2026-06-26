import random


def should_inject_anomaly(probability=0.03):
    """
    Returns True about 3% of the time.
    """
    return random.random() < probability