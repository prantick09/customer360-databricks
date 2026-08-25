import random
import pandas as pd

from faker import Faker

from config import PRODUCT_COUNT, DATA_DIR, RANDOM_SEED

fake = Faker()
Faker.seed(RANDOM_SEED)
random.seed(RANDOM_SEED)


def generate_products():

    categories = {
        "Electronics": [
            "Laptop",
            "Mobile",
            "Headphones",
            "Monitor",
            "Keyboard",
        ],
        "Fashion": [
            "T-Shirt",
            "Jeans",
            "Shoes",
            "Jacket",
            "Watch",
        ],
        "Home": [
            "Chair",
            "Table",
            "Lamp",
            "Sofa",
            "Cookware",
        ],
        "Beauty": [
            "Perfume",
            "Face Wash",
            "Moisturizer",
            "Shampoo",
        ],
    }

    records = []

    for product_id in range(1, PRODUCT_COUNT + 1):

        category = random.choice(list(categories.keys()))

        product_name = random.choice(categories[category])

        records.append(
            {
                "product_id": f"P{product_id:06d}",
                "product_name": product_name,
                "category": category,
                "brand": fake.company(),
                "price": round(random.uniform(200, 150000), 2),
            }
        )

    df = pd.DataFrame(records)

    output_dir = DATA_DIR / "products"
    output_dir.mkdir(parents=True, exist_ok=True)

    df.to_csv(
        output_dir / "products.csv",
        index=False,
    )

    print(f"Generated {len(df)} products")


if __name__ == "__main__":
    generate_products()