from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from cc_shop.models import Product, Purchase  # Adjust 'app' to your actual app name
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Populates the database with random customers and purchases'

    def add_arguments(self, parser):
        parser.add_argument('-n', '--num', type=int, help='Number of purchases to create')

    def handle(self, *args, **options):
        fake = Faker()

        num_purchases = options['num'] if options['num'] else 10  # Default to 10 purchases

        # Generate random users (customers)
        for _ in range(num_purchases):
            user = User.objects.create_user(username=fake.user_name(), email=fake.email())
            user.set_password('12345')  # Simple default password
            user.save()

            # Assume a simple Product model with a fixed price for simplicity
            product = random.choice(Product.objects.all())  # Randomly select a product
            Purchase.objects.create(
                user=user,
                product=product,
                quantity=random.randint(1, 10),  # Random quantity
                status='Completed'
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully added {num_purchases} purchases.'))