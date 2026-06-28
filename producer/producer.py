import json
import time

from kafka import KafkaProducer

from producer.transaction_generator import (
    generate_transaction,
)

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda value: json.dumps(
        value
    ).encode("utf-8"),
)

print("Producer started...\n")

while True:

    transaction = generate_transaction()

    producer.send(
        "payment-transactions",
        transaction.to_dict(),
    )

    producer.flush()

    print(transaction)

    time.sleep(2)