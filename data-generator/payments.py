import random
import pandas as pd

from faker import Faker

from config import (
    PAYMENT_COUNT,
    CUSTOMER_COUNT,
    ORDER_COUNT,
    DATA_DIR,
    RANDOM_SEED,
)

fake = Faker()
Faker.seed(RANDOM_SEED)
random.seed(RANDOM_SEED)


def generate_payments():

    payment_methods = [
        "UPI",
        "CREDIT_CARD",
        "DEBIT_CARD",
        "NET_BANKING",
        "WALLET",
    ]

    payment_statuses = [
        "SUCCESS",
        "FAILED",
        "PENDING",
        "REFUNDED",
    ]

    records = []

    for payment_number in range(
        1,
        PAYMENT_COUNT + 1,
    ):

        order_number = random.randint(
            1,
            ORDER_COUNT,
        )

        records.append(
            {
                "payment_id": f"PAY{payment_number:08d}",
                "order_id": f"ORD{order_number:08d}",
                "customer_id": random.randint(
                    100001,
                    100000 + CUSTOMER_COUNT,
                ),
                "amount": round(
                    random.uniform(200, 100000),
                    2,
                ),
                "payment_method": random.choice(
                    payment_methods
                ),
                "payment_status": random.choice(
                    payment_statuses
                ),
                "transaction_timestamp": fake.date_time_between(
                    start_date="-90d",
                    end_date="now",
                ),
            }
        )

    df = pd.DataFrame(records)

    # Introduce a small number of invalid records
    invalid_count = int(len(df) * 0.01)

    invalid_indexes = random.sample(
        range(len(df)),
        invalid_count,
    )

    df.loc[
        invalid_indexes,
        "amount",
    ] *= -1

    output_dir = DATA_DIR / "payments"
    output_dir.mkdir(parents=True, exist_ok=True)

    df.to_csv(
        output_dir / "payments.csv",
        index=False,
    )

    print(f"Generated {len(df)} payments")


if __name__ == "__main__":
    generate_payments()