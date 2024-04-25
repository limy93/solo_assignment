import random
from cc_shop.models import Product, Purchase
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker

class Command(BaseCommand):
    help = 'Populate the database with random customers and purchases'

    def add_arguments(self, parser):
        # Arguments to specify minimum and maximum number of purchases
        parser.add_argument('-min', '--min_num', type=int, default=10, help='Minimum number of purchases to be created')
        parser.add_argument('-max', '--max_num', type=int, default=30, help='Maximum number of purchases to be created')

    def handle(self, *args, **options):
        fake = Faker()

        # Generate a random number of purchases within the provided range
        min_purchases = options['min_num']
        max_purchases = options['max_num']
        num_purchases = random.randint(min_purchases, max_purchases)

        # Generate random users (customers)
        for _ in range(num_purchases):
            user = User.objects.create_user(username=fake.user_name(), email=fake.email())
            user.set_password('12345')   # Simple default password
            user.save()

            # Assume a simple Product model with a fixed price for simplicity
            product = random.choice(Product.objects.all())   # Randomly select a product
            Purchase.objects.create(
                user=user,
                product=product,
                quantity=random.randint(1, 10),   # Random quantity
                status='Completed'
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully added {num_purchases} purchases.'))