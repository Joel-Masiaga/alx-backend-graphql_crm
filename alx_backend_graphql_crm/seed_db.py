import os
import django
import random
from datetime import datetime, timedelta
from decimal import Decimal

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alx_backend_graphql_crm.settings")
django.setup()

from crm.models import Customer, Product, Order

# === Clear existing data ===
Order.objects.all().delete()
Customer.objects.all().delete()
Product.objects.all().delete()

# === Create Customers ===
customers = []
for i in range(5):
    customer = Customer.objects.create(
        name=f"Customer {i+1}",
        email=f"customer{i+1}@example.com",
        phone=f"+25470000000{i}"
    )
    customers.append(customer)
print(f"Created {len(customers)} customers.")

# === Create Products ===
products = []
for i in range(8):
    product = Product.objects.create(
        name=f"Product {i+1}",
        price=Decimal(f"{random.randint(100, 1000)}.99"),
        stock=random.randint(10, 50)
    )
    products.append(product)
print(f"Created {len(products)} products.")

# === Create Orders ===
for i in range(6):
    customer = random.choice(customers)
    selected_products = random.sample(products, k=random.randint(1, 4))
    total_amount = sum(p.price for p in selected_products)

    order = Order.objects.create(
        customer=customer,
        total_amount=total_amount,
        order_date=datetime.now() - timedelta(days=random.randint(0, 30))
    )
    order.products.set(selected_products)

print("Created 6 sample orders.")
