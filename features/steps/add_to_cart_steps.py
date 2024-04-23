from behave import given, when, then
from django.contrib.auth.models import User
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from uuid import uuid4

@given('I am a registered user')
def step_impl(context):
    unique_username = f"testuser_{uuid4()}"
    context.user = User.objects.create_user(username=unique_username, password='testpassword')
    context.user.save()

@given('I am logged in')
def step_impl(context):
    context.browser.get('http://127.0.0.1:8000/accounts/login/')
    context.browser.find_element(By.NAME, 'username').send_keys(context.user.username)
    context.browser.find_element(By.NAME, 'password').send_keys('testpassword')
    context.browser.find_element(By.TAG_NAME, 'form').submit()
    WebDriverWait(context.browser, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'body'))
    )

@given('I am on the products listing page')
def step_impl(context):
    context.browser.get('http://127.0.0.1:8000/products/')

@when('I click the "Add to Cart" button for a product')
def step_impl(context):
    add_button = context.browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    add_button.click()

@then('I should be redirected to the cart detail page and see the product has been added to my cart for later purchase')
def step_impl(context):
    assert 'Cart' in context.browser.title