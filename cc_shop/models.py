from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone

class Country(models.Model):
    country_code = models.CharField(max_length=3, primary_key=True)
    country_name = models.CharField(max_length=100)

    def __str__(self):
        return self.country_name

class Product(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='products')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=50)   # Types could be like "Carbon Offset", "Renewable Energy Credit", etc
    def __str__(self):
        return f"{self.type} in {self.country.country_name} - ${self.price}"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

class CountryMetadata(models.Model):
    country = models.OneToOneField(Country, on_delete=models.CASCADE, primary_key=True, related_name='metadata')
    long_name = models.CharField(max_length=100)
    region = models.CharField(max_length=50, null=True, blank=True)
    currency_unit = models.CharField(max_length=50, null=True, blank=True)
    income_group = models.CharField(max_length=50, null=True, blank=True)
    special_notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Metadata for {self.country.country_name}"

class ElectricConsumption(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='electric_consumptions')
    year = models.IntegerField()
    consumption = models.FloatField(null=True, blank=True)   # Allow null for years with no data

    def __str__(self):
        return f"{self.country.country_name} {self.year} Consumption"

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)   # Allow null temporarily
    quantity = models.IntegerField(default=1)
    purchase_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, default='Pending')

    @property
    def total_price(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f'{self.user.username} purchased {self.quantity} x {self.product.type} for {self.product.country.country_name} at ${self.product.price} each'