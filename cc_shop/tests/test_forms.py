from cc_shop.forms import ProductForm, RegisterForm
from cc_shop.models import Country
from django.test import TestCase

class ProductFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.country = Country.objects.create(country_code='USA', country_name='United States')

    def test_product_form_valid_data(self):
        form = ProductForm(data={'country': self.country.pk, 'price': '49.99'})
        self.assertTrue(form.is_valid())

    def test_product_form_invalid_data(self):
        form = ProductForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('country', form.errors)
        self.assertIn('price', form.errors)

class RegisterFormTest(TestCase):
    def test_register_form_valid_data(self):
        form = RegisterForm(data={
            'username': 'newuser',
            'email': 'user@example.com',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123'
        })
        self.assertTrue(form.is_valid())

    def test_register_form_password_mismatch(self):
        form = RegisterForm(data={
            'username': 'newuser',
            'email': 'user@example.com',
            'password1': 'complexpassword123',
            'password2': 'differentpassword123'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)