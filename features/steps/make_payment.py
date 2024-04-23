from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@given('I am logged in with valid credentials')
def step_impl(context):
    # Navigate to login page
    context.browser.get('http://127.0.0.1:8000/accounts/login/')
    
    # Fill login form and submit
    username_input = context.browser.find_element(By.ID, 'id_username')
    password_input = context.browser.find_element(By.ID, 'id_password')
    username_input.send_keys('user@example.com')
    password_input.send_keys('securepassword123')
    login_button = context.browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    login_button.click()
    # Validate successful login by checking for a specific element that appears only when logged in
    WebDriverWait(context.browser, 10).until(
        EC.visibility_of_element_located((By.ID, 'logout_link'))  # Assuming there's a logout link or similar indication
    )

@given('I am on the Make Payment page')
def step_impl(context):
    context.browser.get(context.get_url('make_payment'))  # Adjust the URL getter to your context setup.

@when('I fill in the payment form with valid details')
def step_impl(context):
    WebDriverWait(context.browser, 10).until(
        EC.visibility_of_element_located((By.ID, 'cardName'))).send_keys('John Doe')
    context.browser.find_element(By.ID, 'cardNumber').send_keys('4111111111111111')
    context.browser.find_element(By.ID, 'cardExpiry').send_keys('1224')
    context.browser.find_element(By.ID, 'cardCVV').send_keys('123')

@when('I click the "Submit Payment" button')
def step_impl(context):
    submit_button = context.browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    submit_button.click()

@then('I should be redirected to the Payment Status page')
def step_impl(context):
    WebDriverWait(context.browser, 10).until(
        EC.url_contains('payment_status'))  # Adjust the URL check based on actual application behavior.

@then('I should see a payment success message')
def step_impl(context):
    success_message = WebDriverWait(context.browser, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '.success')))  # Adjust selector to match your success message element.
    assert 'Payment Successful' in success_message.text