import random
import pandas as pd

from faker import Faker

from config import (
    ORDER_COUNT,
    CUSTOMER_COUNT,
    PRODUCT_COUNT,
    DATA_DIR,
    RANDOM_SEED,
)

fake = Faker()
Faker.seed(RANDOM_SEED)
random.seed(RANDOM_SEED)


def generate_orders():

    records = []

    statuses = [
        "PLACED",
        "SHIPPED",
        "DELIVERED",
        "CANCELLED",
    ]

    for order_number in range(1, ORDER_COUNT + 1):

        customer_id = random.randint(
            100001,
            100000 + CUSTOMER_COUNT,
        )

        product_id = f"P{random.randint(1, PRODUCT_COUNT):06d}"

        quantity = random.randint(1, 5)

        price = round(random.uniform(200, 150000), 2)

        amount = round(price * quantity, 2)

        records.append(
            {
                "order_id": f"ORD{order_number:08d}",
                "customer_id": customer_id,
                "product_id": product_id,
                "quantity": quantity,
                "order_amount": amount,
                "order_status": random.choice(statuses),
                "order_timestamp": fake.date_time_between(
                    start_date="-90d",
                    end_date="now",
                ),
            }
        )

    df = pd.DataFrame(records)

    # -------------------------------------------------
    # Introduce bad data intentionally
    # -------------------------------------------------

    # 1% NULL customer IDs
    null_count = int(len(df) * 0.01)

    null_indexes = random.sample(
        range(len(df)),
        null_count,
    )

    df.loc[
        null_indexes,
        "customer_id",
    ] = None

    # 1% negative amounts
    negative_count = int(len(df) * 0.01)

    negative_indexes = random.sample(
        range(len(df)),
        negative_count,
    )

    df.loc[
        negative_indexes,
        "order_amount",
    ] *= -1

    # Duplicate 2% of records
    duplicate_count = int(len(df) * 0.02)

    duplicates = df.sample(
        duplicate_count,
        random_state=RANDOM_SEED,
    )

    df = pd.concat(
        [df, duplicates],
        ignore_index=True,
    )

    output_dir = DATA_DIR / "orders"
    output_dir.mkdir(parents=True, exist_ok=True)

    df.to_csv(
        output_dir / "orders.csv",
        index=False,
    )

    print(f"Generated {len(df)} order records")


if __name__ == "__main__":
    generate_orders()