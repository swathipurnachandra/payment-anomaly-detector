import math
from datetime import datetime

from redis_store.user_state import get_last_city, get_last_seen


# Approximate city coordinates (latitude, longitude)
CITY_COORDS = {
    "Chennai": (13.0827, 80.2707),
    "Bengaluru": (12.9716, 77.5946),
    "Hyderabad": (17.3850, 78.4867),
    "Mumbai": (19.0760, 72.8777),
    "Delhi": (28.6139, 77.2090),
    "Pune": (18.5204, 73.8567),
    "Kolkata": (22.5726, 88.3639),
    "Ahmedabad": (23.0225, 72.5714),
    "Jaipur": (26.9124, 75.7873),
    "Kochi": (9.9312, 76.2673),
    "Lucknow": (26.8467, 80.9462),
    "Indore": (22.7196, 75.8577),
}

# A common formula for distance between two lat/long points
def haversine_km(lat1, lon1, lat2, lon2):
    radius_km = 6371.0

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_phi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return radius_km * c


def check_impossible_travel(transaction: dict) -> tuple[bool, str | None]:
    user_id = transaction["user_id"]
    current_city = transaction["city"]
    current_event_time = transaction["event_time"]

    previous_city = get_last_city(user_id)
    previous_timestamp = get_last_seen(user_id)

    if not previous_city or not previous_timestamp:
        return False, None

    if previous_city == current_city:
        return False, None

    previous_lat, previous_lon = CITY_COORDS.get(previous_city, (None, None))
    current_lat, current_lon = CITY_COORDS.get(current_city, (None, None))

    if previous_lat is None or previous_lon is None:
        return False, None
    if current_lat is None or current_lon is None:
        return False, None

    # elapsed time in hours
    previous_time_epoch = iso_to_epoch(previous_timestamp)
    elapsed_seconds = current_event_time - int(previous_time_epoch)
    if elapsed_seconds <= 0:
        return False, None

    elapsed_hours = elapsed_seconds / 3600

    if elapsed_hours == 0:
        return False, None

    distance_km = haversine_km(
        previous_lat,
        previous_lon,
        current_lat,
        current_lon,
    )

    implied_speed_kmh = distance_km / elapsed_hours

    # A simple threshold for "too far too fast"
    if distance_km > 300 and implied_speed_kmh > 500:
        return True, "Impossible Travel"

    return False, None

def iso_to_epoch(value: str) -> int:
    return int(datetime.fromisoformat(value).timestamp())