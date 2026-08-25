import random
import pandas as pd

from faker import Faker

from config import (
    TICKET_COUNT,
    CUSTOMER_COUNT,
    DATA_DIR,
    RANDOM_SEED,
)

fake = Faker()
Faker.seed(RANDOM_SEED)
random.seed(RANDOM_SEED)


def generate_support_tickets():

    categories = [
        "PAYMENT",
        "REFUND",
        "DELIVERY",
        "PRODUCT",
        "ACCOUNT",
    ]

    priorities = [
        "LOW",
        "MEDIUM",
        "HIGH",
        "CRITICAL",
    ]

    statuses = [
        "OPEN",
        "IN_PROGRESS",
        "RESOLVED",
        "CLOSED",
    ]

    records = []

    for ticket_number in range(
        1,
        TICKET_COUNT + 1,
    ):

        records.append(
            {
                "ticket_id": f"TKT{ticket_number:08d}",
                "customer_id": random.randint(
                    100001,
                    100000 + CUSTOMER_COUNT,
                ),
                "category": random.choice(
                    categories
                ),
                "priority": random.choice(
                    priorities
                ),
                "description": fake.sentence(
                    nb_words=15
                ),
                "status": random.choice(
                    statuses
                ),
                "created_at": fake.date_time_between(
                    start_date="-90d",
                    end_date="now",
                ),
            }
        )

    df = pd.DataFrame(records)

    output_dir = DATA_DIR / "support_tickets"
    output_dir.mkdir(parents=True, exist_ok=True)

    df.to_csv(
        output_dir / "support_tickets.csv",
        index=False,
    )

    print(
        f"Generated {len(df)} support tickets"
    )


if __name__ == "__main__":
    generate_support_tickets()