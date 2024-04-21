from cc_shop.models import Cart, CartItem, Country, Product, User
from django.test import TestCase
from django.urls import reverse

class ECommerceIntegrationTests(TestCase):
    def setUp(self):
        # Set up the necessary data for each test
        self.country = Country.objects.create(country_code='US', country_name='United States')
        self.product = Product.objects.create(country=self.country, description='Solar Panel', price=299.99, type='Renewable Energy')

    def test_user_registration_and_login(self):
        # Attempt to register a new user
        response = self.client.post(reverse('register'), data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'complexpassword',
            'password2': 'complexpassword'
        })
        
        self.assertEqual(response.status_code, 302, "Should redirect after registration")
        
        # Check if the user actually exists in the database
        user_exists = User.objects.filter(username='newuser').exists()
        self.assertTrue(user_exists, "User should exist in the database after registration")
        
        if user_exists:
            user = User.objects.get(username='newuser')
            self.assertTrue(user.is_active, "User should be active after registration")
            logged_in = self.client.login(username='newuser', password='complexpassword')
            self.assertTrue(logged_in, "User should be logged in successfully")

    def test_add_product_to_cart(self):
        # Pre-create and log in a user
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        # Add a product to the cart
        response = self.client.post(reverse('add_to_cart', args=[self.product.id]))
        self.assertRedirects(response, reverse('cart_detail'))
        # Check cart items
        cart = Cart.objects.get(user=self.user, active=True)
        self.assertEqual(cart.items.count(), 1)
        self.assertEqual(cart.items.first().product, self.product)

    def test_checkout_process(self):
        # Pre-create and log in a user
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        # Simulate adding product to cart
        cart = Cart.objects.create(user=self.user, active=True)
        CartItem.objects.create(cart=cart, product=self.product, quantity=1)
        # Checkout process
        response = self.client.post(reverse('checkout'))
        self.assertRedirects(response, reverse('make_payment'))
        # Simulate payment
        payment_response = self.client.post(reverse('make_payment'), {
            'cardName': 'Test User',
            'cardNumber': '4111111111111111',
            'cardExpiry': '12/24',
            'cardCVV': '123'
        })
        self.assertRedirects(payment_response, reverse('payment_status'))
