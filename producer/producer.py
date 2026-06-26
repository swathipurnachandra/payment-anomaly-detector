from kafka import KafkaProducer
import json
import time

from producer.transaction_generator import generate_transaction

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

print("Producer started...\n")

while True:
    transaction = generate_transaction()

    producer.send("payment-transactions", transaction)
    producer.flush()

    print(transaction)

    time.sleep(2)