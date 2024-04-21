from cc_shop.admin import CountryAdmin, ProductAdmin
from cc_shop.models import Country, Product
from django.contrib.auth.models import User
from django.contrib.admin.sites import AdminSite
from django.test import TestCase, RequestFactory

class MockRequest:
    def __init__(self):
        self.user = User()

class ProductAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.factory = RequestFactory()
        self.admin_user = User.objects.create_superuser('admin', 'admin@test.com', 'password')
        self.client.login(username='admin', password='password')
        self.country = Country.objects.create(country_code='USA', country_name='United States')
        self.product = Product.objects.create(country=self.country, description='Test Product', price=99.99, type='Test Type')

    def test_product_admin_list_display(self):
        ma = ProductAdmin(Product, self.site)
        request = self.factory.get('/')
        request.user = self.admin_user
        queryset = ma.get_queryset(request)
        self.assertIn(self.product, queryset)
        self.assertEqual(ma.list_display, ('description', 'price', 'country'))

class CountryAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.country = Country.objects.create(country_code='GB', country_name='United Kingdom')

    def test_country_admin_search_fields(self):
        ca = CountryAdmin(Country, self.site)
        self.assertEqual(ca.search_fields, ('country_name', 'country_code'))