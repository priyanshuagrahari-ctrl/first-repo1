import random
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from products.models import Product


class Command(BaseCommand):
    help = "Insert 1 lakh random products"

    def handle(self, *args, **kwargs):
        total_records = 100_000
        batch_size = 1000
        products = []

        self.stdout.write("Starting product insertion...")

        with transaction.atomic():
            for i in range(1, total_records + 1):
                products.append(
                    Product(
                        name=f"Product {i}",
                        price=Decimal(random.randint(100, 100000)) / 100
                    )
                )

                if len(products) == batch_size:
                    Product.objects.bulk_create(products)
                    products = []

                if i % 10_000 == 0:
                    self.stdout.write(f"{i} products inserted...")

            if products:
                Product.objects.bulk_create(products)

        self.stdout.write(
            self.style.SUCCESS("Successfully inserted 1 lakh products")
        )
