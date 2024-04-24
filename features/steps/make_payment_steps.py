from behave import given, when, then
from django.contrib.auth.models import User
from cc_shop.models import Product, Cart, CartItem, Country
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from uuid import uuid4

@given('I have already registered')
def step_impl(context):
    unique_username = f"testuser_{uuid4()}"
    context.user = User.objects.create_user(username=unique_username, password='testpassword')
    context.user.save()

@given('I have logged in to my account')
def step_impl(context):
    context.browser.get('http://127.0.0.1:8000/accounts/login/')
    context.browser.find_element(By.NAME, 'username').send_keys(context.user.username)
    context.browser.find_element(By.NAME, 'password').send_keys('testpassword')
    context.browser.find_element(By.TAG_NAME, 'form').submit()
    WebDriverWait(context.browser, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'body'))
    )

@given('products are added to my cart')
def step_impl(context):
    cart, _ = Cart.objects.get_or_create(user=context.user, active=True)
    country_us, _ = Country.objects.update_or_create(country_code="US", defaults={'country_name': "USA"})
    country_ca, _ = Country.objects.update_or_create(country_code="CA", defaults={'country_name': "Canada"})

    product1, _ = Product.objects.update_or_create(
        country=country_us,
        defaults={'description': "Dummy Product 1", 'price': 100, 'type': "Type1"}
    )
    product2, _ = Product.objects.update_or_create(
        country=country_ca,
        defaults={'description': "Dummy Product 2", 'price': 200, 'type': "Type2"}
    )
    CartItem.objects.update_or_create(cart=cart, product=product1, defaults={'quantity': 1})
    CartItem.objects.update_or_create(cart=cart, product=product2, defaults={'quantity': 1})

    context.cart = cart
    assert CartItem.objects.filter(cart=cart).count() > 0, "Cart is empty"

@given('I am on the Make Payment page')
def step_impl(context):
    context.browser.get('http://127.0.0.1:8000/make_payment/')
    assert 'make_payment' in context.browser.current_url

@when('I fill in the payment form with valid details')
def step_impl(context):
    context.browser.find_element(By.ID, 'cardName').send_keys('John Doe')
    context.browser.find_element(By.ID, 'cardNumber').send_keys('1234567890123456')
    context.browser.find_element(By.ID, 'cardExpiry').send_keys('12/24')
    context.browser.find_element(By.ID, 'cardCVV').send_keys('123')
    context.payment_form_data = {
        'cardName': 'John Doe',
        'cardNumber': '1234567890123456',
        'cardExpiry': '12/24',
        'cardCVV': '123'
    }

@when('I click the "Submit Payment" button')
def step_impl(context):
    context.browser.find_element(By.TAG_NAME, 'form').submit()

@then('I should be redirected to the Payment Status page')
def step_impl(context):
    WebDriverWait(context.browser, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'body'))
    )
    assert 'payment_status' in context.browser.current_url

@then('I should see a payment success message')
def step_impl(context):
    # Wait for any message to be visible that has the 'text-success' class indicating a successful operation
    WebDriverWait(context.browser, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'text-success'))
    )
    success_message = context.browser.find_element(By.CLASS_NAME, 'text-success').text
    assert 'Payment successful' in success_message