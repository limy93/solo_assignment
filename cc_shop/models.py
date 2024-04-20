from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

# Create your models here.

class Country(models.Model):
    country_code = models.CharField(max_length=3, primary_key=True)
    country_name = models.CharField(max_length=100)

    def __str__(self):
        return self.country_name

class ElectricConsumption(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='electric_consumptions')
    year = models.IntegerField()
    consumption = models.FloatField(null=True, blank=True)  # Allows null for years with no data

    def __str__(self):
        return f"{self.country.country_name} {self.year} Consumption"

class CountryMetadata(models.Model):
    country = models.OneToOneField(Country, on_delete=models.CASCADE, primary_key=True, related_name='metadata')
    long_name = models.CharField(max_length=100)
    region = models.CharField(max_length=50, null=True, blank=True)
    currency_unit = models.CharField(max_length=50, null=True, blank=True)
    income_group = models.CharField(max_length=50, null=True, blank=True)
    special_notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Metadata for {self.country.country_name}"

class Product(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='products')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=50)  # Types could be like "Renewable Energy Credit", "Carbon Offset", etc.

    def __str__(self):
        return f"{self.type} in {self.country.country_name} - ${self.price}"

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)  # Allow null temporarily
    quantity = models.IntegerField(default=1)
    purchase_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, default='Pending')

    @property
    def total_price(self):
        return self.quantity * self.product.price
    
    def __str__(self):
        return f'{self.user.username} purchased {self.quantity} x {self.product.type} for {self.product.country.country_name} at ${self.product.price} each'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    # Additional fields can be added here

    def __str__(self):
        return f"{self.user.username}'s Profile"

# Create or update a Profile automatically whenever a User instance is created or updated
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)