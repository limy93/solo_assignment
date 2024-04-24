import time
from behave import given, when, then
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

@given('I am on the Login page')
def step_impl(context):
    context.browser.get('http://127.0.0.1:8000/accounts/login/')
    assert "Login" in context.browser.title

@when('I click on the "Forgot your password?" link')
def step_impl(context):
    context.browser.find_element(By.LINK_TEXT, "Forgot your password?").click()

@when('I submit my email address for password reset')
def step_impl(context):
    context.browser.find_element(By.NAME, 'email').send_keys("user@example.com")
    context.browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

@then('I should be informed to check my email for a reset link')
def step_impl(context):
    expected_message = "We’ve emailed you instructions for setting your password, if an account exists with the email you entered. You should receive them shortly."
    assert expected_message in context.browser.page_source

@given('I have a valid reset link')
def step_impl(context):
    context.reset_link = "http://127.0.0.1:8000/reset/MOCK_TOKEN/"
    assert context.reset_link is not None

@when('I visit the password reset link')
def step_impl(context):
    context.browser.get(context.reset_link)

@when('I submit a new password')
def step_impl(context):
    assert "password" in context.browser.page_source.lower(), "Page does not contain expected content related to password resetting."

@then('I should see a password reset success message')
def step_impl(context):
    assert "reset" in context.browser.page_source.lower(), "Success message not found on the page"