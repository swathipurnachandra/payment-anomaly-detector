from kafka import KafkaConsumer
from redis_store.state_manager import ensure_user_state, process_transaction
import json
from detector.detector import detect

consumer = KafkaConsumer(
    "payment-transactions",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

print("Consumer started...\n")

for message in consumer:
    transaction = message.value

    # Initialize the baseline before detection, but preserve the previous
    # city and timestamp until the location rule has evaluated this event.
    ensure_user_state(transaction["user_id"])
    result = detect(transaction)
    state = process_transaction(transaction)

    transaction["detected_anomaly"] = result["is_anomaly"]
    transaction["detected_reasons"] = result["reasons"]

    print(transaction)
    print(state)
    print(result)
    print("-" * 60)