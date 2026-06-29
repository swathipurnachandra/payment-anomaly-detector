from kafka import KafkaConsumer
from redis_store.state_manager import process_transaction
import json

consumer = KafkaConsumer(
    "payment-transactions",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

print("Consumer started...\n")

for message in consumer:

    transaction = message.value

    state = process_transaction(transaction)

    print()

    print(transaction)

    print(state)

    print("-" * 60)