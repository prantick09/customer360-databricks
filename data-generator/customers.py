import random
import pandas as pd

from faker import Faker

from config import CUSTOMER_COUNT, DATA_DIR, RANDOM_SEED

fake = Faker()
Faker.seed(RANDOM_SEED)
random.seed(RANDOM_SEED)


def generate_customers():
    records = []

    cities = [
        "Kolkata",
        "Mumbai",
        "Delhi",
        "Bangalore",
        "Hyderabad",
        "Chennai",
        "Pune",
        "Ahmedabad",
    ]

    segments = [
        "BRONZE",
        "SILVER",
        "GOLD",
        "PLATINUM",
    ]

    for customer_id in range(100001, 100001 + CUSTOMER_COUNT):

        records.append(
            {
                "customer_id": customer_id,
                "name": fake.name(),
                "email": fake.email(),
                "phone": fake.phone_number(),
                "city": random.choice(cities),
                "country": "India",
                "segment": random.choice(segments),
                "signup_date": fake.date_between(
                    start_date="-3y",
                    end_date="today",
                ),
            }
        )

    df = pd.DataFrame(records)

    output_dir = DATA_DIR / "customers"
    output_dir.mkdir(parents=True, exist_ok=True)

    df.to_csv(
        output_dir / "customers.csv",
        index=False,
    )

    print(f"Generated {len(df)} customers")


if __name__ == "__main__":
    generate_customers()