import random
import uuid
import pandas as pd

from faker import Faker

from config import (
    CLICKSTREAM_COUNT,
    CUSTOMER_COUNT,
    DATA_DIR,
    RANDOM_SEED,
)

fake = Faker()
Faker.seed(RANDOM_SEED)
random.seed(RANDOM_SEED)


def generate_clickstream():

    event_types = [
        "PAGE_VIEW",
        "SEARCH",
        "PRODUCT_VIEW",
        "ADD_TO_CART",
        "CHECKOUT",
        "PURCHASE",
    ]

    devices = [
        "MOBILE",
        "DESKTOP",
        "TABLET",
    ]

    pages = [
        "/",
        "/products",
        "/electronics",
        "/fashion",
        "/cart",
        "/checkout",
    ]

    records = []

    for _ in range(CLICKSTREAM_COUNT):

        records.append(
            {
                "event_id": str(uuid.uuid4()),
                "customer_id": random.randint(
                    100001,
                    100000 + CUSTOMER_COUNT,
                ),
                "session_id": str(uuid.uuid4()),
                "event_type": random.choice(
                    event_types
                ),
                "page": random.choice(pages),
                "device": random.choice(devices),
                "ip_address": fake.ipv4(),
                "event_timestamp": fake.date_time_between(
                    start_date="-30d",
                    end_date="now",
                ),
            }
        )

    df = pd.DataFrame(records)

    output_dir = DATA_DIR / "clickstream"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Write in chunks/files instead of one huge file.
    chunk_size = 100_000

    for i, start in enumerate(
        range(0, len(df), chunk_size)
    ):

        chunk = df.iloc[
            start:start + chunk_size
        ]

        chunk.to_csv(
            output_dir / f"clickstream_{i:04d}.csv",
            index=False,
        )

    print(
        f"Generated {len(df)} clickstream events"
    )


if __name__ == "__main__":
    generate_clickstream()