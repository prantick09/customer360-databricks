import json
import random
import time
import uuid
from datetime import datetime, timezone, timedelta

from faker import Faker
from kafka import KafkaProducer

from config import CUSTOMER_COUNT, PRODUCT_COUNT, RANDOM_SEED


fake = Faker()
Faker.seed(RANDOM_SEED)
random.seed(RANDOM_SEED)


BOOTSTRAP_SERVERS = "localhost:9092"


producer = KafkaProducer(
    bootstrap_servers=BOOTSTRAP_SERVERS,
    value_serializer=lambda value: json.dumps(value).encode("utf-8"),
)

def generate_event_time():
    event_time = datetime.now(timezone.utc)

    #5% late events
    if random.random() < 0.05:
        event_time -=timedelta(minutes=random.randint(1,20))

    return event_time.isoformat()


def generate_order_event():
    customer_id = random.randint(
        100001,
        100000 + CUSTOMER_COUNT,
    )

    if random.random() <0.01:
        customer_id = None

    product_id = f"P{random.randint(1, PRODUCT_COUNT):06d}"

    quantity = random.randint(1, 5)

    amount = round(
        random.uniform(200, 100000) * quantity,
        2,
    )

    return {
        "event_id": str(uuid.uuid4()),
        "event_type": "ORDER",
        "order_id": f"ORD-{uuid.uuid4().hex[:12]}",
        "customer_id": customer_id,
        "product_id": product_id,
        "quantity": quantity,
        "amount": amount,
        "order_status": random.choice(
            [
                "PLACED",
                "SHIPPED",
                "DELIVERED",
            ]
        ),
        "event_time": generate_event_time(),
    }


def generate_payment_event():
    customer_id = random.randint(
        100001,
        100000 + CUSTOMER_COUNT,
    )

    if random.random() <0.01:
            customer_id = None

    amount = round(
        random.uniform(200, 100000),
        2,
    )

    return {
        "event_id": str(uuid.uuid4()),
        "event_type": "PAYMENT",
        "payment_id": f"PAY-{uuid.uuid4().hex[:12]}",
        "customer_id": customer_id,
        "amount": amount,
        "payment_method": random.choice(
            [
                "UPI",
                "CREDIT_CARD",
                "DEBIT_CARD",
                "NET_BANKING",
                "WALLET",
            ]
        ),
        "payment_status": random.choice(
            [
                "SUCCESS",
                "FAILED",
                "PENDING",
            ]
        ),
        "event_time": generate_event_time(),
    }


def generate_clickstream_event():
    customer_id = random.randint(
        100001,
        100000 + CUSTOMER_COUNT,
    )

    if random.random() <0.01:
            customer_id = None

    return {
        "event_id": str(uuid.uuid4()),
        "event_type": "CLICKSTREAM",
        "customer_id": customer_id,
        "session_id": str(uuid.uuid4()),
        "action": random.choice(
            [
                "PAGE_VIEW",
                "SEARCH",
                "PRODUCT_VIEW",
                "ADD_TO_CART",
                "CHECKOUT",
                "PURCHASE",
            ]
        ),
        "page": random.choice(
            [
                "/",
                "/products",
                "/electronics",
                "/fashion",
                "/cart",
                "/checkout",
            ]
        ),
        "device": random.choice(
            [
                "MOBILE",
                "DESKTOP",
                "TABLET",
            ]
        ),
        "event_time": generate_event_time(),
    }


def generate_normal_transaction():

    customer_id = random.randint(
        100001,
        100000 + CUSTOMER_COUNT,
    )

    amount = round(
        random.uniform(200, 10000),
        2,
    )

    return {
        "event_id": str(uuid.uuid4()),
        "event_type": "TRANSACTION",
        "transaction_id": f"TX-{uuid.uuid4().hex[:12]}",
        "customer_id": customer_id,
        "amount": amount,
        "city": random.choice(
            [
                "Kolkata",
                "Mumbai",
                "Delhi",
                "Bangalore",
            ]
        ),
        "payment_method": random.choice(
            [
                "UPI",
                "CREDIT_CARD",
                "DEBIT_CARD",
                "NET_BANKING",
            ]
        ),
        "event_time": generate_event_time(),
    }


def generate_fraud_event():

    customer_id = random.randint(
        100001,
        100000 + CUSTOMER_COUNT,
    )

    # Occasionally create a missing customer ID
    if random.random() < 0.01:
        customer_id = None

    amount = random.choice(
        [
            90000,
            95000,
            120000,
            150000,
        ]
    )

    return {
        "event_id": str(uuid.uuid4()),
        "event_type": "TRANSACTION",
        "transaction_id": f"TX-{uuid.uuid4().hex[:12]}",
        "customer_id": customer_id,
        "amount": amount,
        "city": random.choice(
            [
                "Kolkata",
                "Mumbai",
                "Delhi",
                "Bangalore",
            ]
        ),
        "payment_method": random.choice(
            [
                "UPI",
                "CREDIT_CARD",
                "DEBIT_CARD",
                "NET_BANKING",
            ]
        ),
        "event_time": generate_event_time(),
    }


def send_event(topic, event):

    producer.send(
        topic,
        value=event,
    )

    # 2% chance of duplicate event
    if random.random() < 0.02:

        time.sleep(0.1)

        producer.send(
            topic,
            value=event,
        )

        print(
            f"[DUPLICATE] {topic} - {event['event_id']}"
        )

    else:

        print(
            f"[{topic}] {event}"
        )


def main():

    print(
        "Starting Customer360 streaming generator..."
    )

    while True:

        event_type = random.choice(
            [
                "order",
                "payment",
                "clickstream",
                "transaction",
                "fraud",
            ]
        )

        if event_type == "order":

            event = generate_order_event()

            send_event(
                "orders",
                event,
            )

        elif event_type == "payment":

            event = generate_payment_event()

            send_event(
                "payments",
                event,
            )

        elif event_type == "clickstream":

            event = generate_clickstream_event()

            send_event(
                "clickstream",
                event,
            )

        elif event_type == "transaction":

            event = generate_normal_transaction()

            send_event(
                "customer-events",
                event
            )

        else:

            event = generate_fraud_event()

            send_event(
                "customer-events",
                event,
            )

        time.sleep(
            random.uniform(0.2, 1.0)
        )


if __name__ == "__main__":
    main()