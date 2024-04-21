from cc_shop.models import Country, Product, Purchase, User
from decimal import Decimal
from django.test import TestCase

class CountryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Country.objects.create(country_code='USA', country_name='United States')

    def test_country_name_label(self):
        country = Country.objects.get(country_code='USA')
        field_label = country._meta.get_field('country_name').verbose_name
        self.assertEqual(field_label, 'country name')

    def test_country_code_label(self):
        country = Country.objects.get(country_code='USA')
        field_label = country._meta.get_field('country_code').verbose_name
        self.assertEqual(field_label, 'country code')

    def test_country_name_max_length(self):
        country = Country.objects.get(country_code='USA')
        max_length = country._meta.get_field('country_name').max_length
        self.assertEquals(max_length, 100)

    def test_object_name_is_country_name(self):
        country = Country.objects.get(country_code='USA')
        expected_object_name = country.country_name
        self.assertEquals(expected_object_name, str(country))

class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a Country object to use as a foreign key
        country = Country.objects.create(country_code='CAN', country_name='Canada')
        Product.objects.create(description='Wind Power Credit', price=Decimal('20.00'), country=country, type='Renewable Energy Credit')

    def test_product_string_representation(self):
        product = Product.objects.get(id=1)
        expected_string = f"{product.type} in {product.country.country_name} - ${product.price}"
        self.assertEquals(expected_string, str(product))

class PurchaseModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='testuser', password='12345')
        country = Country.objects.create(country_code='FRA', country_name='France')
        product = Product.objects.create(description='Solar Power Credit', price=Decimal('15.00'), country=country, type='Carbon Offset')
        Purchase.objects.create(user=user, product=product, quantity=2)

    def test_purchase_total_price(self):
        purchase = Purchase.objects.get(id=1)
        expected_total = Decimal('30.00')  # 2 * 15.00
        self.assertEquals(purchase.total_price, expected_total)

    def test_purchase_string_representation(self):
        purchase = Purchase.objects.get(id=1)
        expected_string = f'{purchase.user.username} purchased {purchase.quantity} x {purchase.product.type} for {purchase.product.country.country_name} at ${purchase.product.price} each'
        self.assertEquals(expected_string, str(purchase))