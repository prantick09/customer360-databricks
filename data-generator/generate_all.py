from customers import generate_customers
from products import generate_products
from orders import generate_orders
from payments import generate_payments
from clickstream import generate_clickstream
from support_tickets import generate_support_tickets


def main():

    print("===================================")
    print("Customer360 Data Generation Started")
    print("===================================")

    generate_customers()

    generate_products()

    generate_orders()

    generate_payments()

    generate_clickstream()

    generate_support_tickets()

    print("===================================")
    print("Data generation completed")
    print("===================================")


if __name__ == "__main__":
    main()