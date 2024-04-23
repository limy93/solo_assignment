from cc_shop.models import Country, Product, Purchase, User
from decimal import Decimal
from django.contrib.auth.models import User
from django.test import TestCase
from django.test import Client
from django.urls import reverse

class HomePageViewTest(TestCase):
    def test_home_page_status_code(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_page_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_contains_correct_html(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Welcome to EpochCraft!')

class AboutPageViewTest(TestCase):
    def test_about_page_status_code(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

    def test_about_page_uses_correct_template(self):
        response = self.client.get(reverse('about'))
        self.assertTemplateUsed(response, 'about.html')

    def test_about_page_contains_correct_html(self):
        response = self.client.get(reverse('about'))
        self.assertContains(response, 'About')

class ProductListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_products = 20
        for product_id in range(number_of_products):
            Product.objects.create(
                description=f'Sample Product {product_id}',
                price=Decimal('22.99'),
                type='Type',
                country=Country.objects.create(country_code=f'CC{product_id}', country_name=f'Country {product_id}')
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('list_products'))
        self.assertTemplateUsed(response, 'list_products.html')

    def test_pagination_is_twenty(self):
        response = self.client.get(reverse('list_products'))
        self.assertIn('products_page_obj', response.context)
        self.assertTrue(response.context['products_page_obj'].has_previous)
        self.assertTrue(response.context['products_page_obj'].has_next)
        self.assertEqual(response.context['products_page_obj'].paginator.count, 20)  # Assuming 20 items per page

    def test_lists_all_products(self):
        response = self.client.get(reverse('list_products'))
        self.assertIn('products_page_obj', response.context)
        self.assertEqual(len(response.context['products_page_obj'].object_list), 20)
        self.assertIn('products_page_obj', response.context)

class DashboardViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up a user for login
        cls.user = User.objects.create_user(username='testuser', password='12345')

    def test_dashboard_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(response, f'/accounts/login/?next=/dashboard/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(str(response.context['user']), 'testuser')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')