from django.core import mail
import re
from behave import given, when, then
from selenium.webdriver.common.by import By
from urllib.parse import urljoin

def get_reset_link():
    # Check there's at least one message in the outbox
    if len(mail.outbox) > 0:
        email_body = mail.outbox[0].body
        # Regular expression to extract URL
        match = re.search(r'http://127\.0\.0\.1:8000/reset/.+/', email_body)
        if match:
            return match.group(0)
    return None

@given('I am on the Login page')
def step_impl(context):
    context.browser.get('http://127.0.0.1:8000/accounts/login/')
    assert "Login" in context.browser.title

@given('I have received the password reset email')
def step_impl(context):
    context.reset_link = get_reset_link()
    assert context.reset_link is not None, "Failed to extract password reset link"

@when('I click on the "Forgot your password?" link')
def step_impl(context):
    context.browser.find_element(By.LINK_TEXT, "Forgot your password?").click()

@when('I submit my email address for password reset')
def step_impl(context):
    context.browser.find_element(By.NAME, 'email').send_keys("user@example.com")
    context.browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

@when('I visit the password reset link')
def step_impl(context):
    context.browser.get(context.reset_link)

@when('I submit a new password')
def step_impl(context):
    context.browser.find_element_by_name('new_password1').send_keys('newsecurepassword123')
    context.browser.find_element_by_name('new_password2').send_keys('newsecurepassword123')
    context.browser.find_element_by_css_selector('form button[type="submit"]').click()

@then('I should receive a password reset link')
def step_impl(context):
    assert len(mail.outbox) == 1
    assert "password reset" in mail.outbox[0].subject
    
@then('I should see a password reset success message')
def step_impl(context):
    success_message = "Your password has been reset. You may go ahead and log in now."
    assert success_message in context.browser.page_source