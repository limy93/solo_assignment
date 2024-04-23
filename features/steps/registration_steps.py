import time
from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def generate_unique_username(base="testuser"):
    """Generate a unique username using a base name and the current timestamp."""
    return f"{base}_{int(time.time())}"
        
@given('I am on the Registration page')
def step_impl(context):
    context.browser.get('http://127.0.0.1:8000/register/')
    assert "Register" in context.browser.title

@when('I enter valid registration details')
def step_impl(context):
    unique_username = generate_unique_username()
    context.browser.find_element(By.NAME, 'username').send_keys(unique_username)
    context.browser.find_element(By.NAME, 'email').send_keys(f"{unique_username}@example.com")
    context.browser.find_element(By.NAME, 'password1').send_keys('securepassword123')
    context.browser.find_element(By.NAME, 'password2').send_keys('securepassword123')

@when('I submit the registration form')
def step_impl(context):
    submit_button = context.browser.find_element(By.XPATH, '//button[@type="submit"]')
    submit_button.click()

@then('I should be registered and redirected to the Dashboard page')
def step_impl(context):
    try:
        WebDriverWait(context.browser, 20).until(
            EC.title_contains("Dashboard")
        )
        assert "Dashboard" in context.browser.title
    except Exception as e:
        raise AssertionError("Dashboard page was not reached after registration.")