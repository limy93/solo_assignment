from behave import given, then
from selenium.webdriver.common.by import By

@given('I am on the Products page')
def step_impl(context):
    context.browser.get('http://127.0.0.1:8000/products/')

@when('I click on the "View Details" button to look for more product details')
def step_impl(context):
    ecocredits_button = context.browser.find_element(By.ID, "view-button")
    ecocredits_button.click()

@then('I should see a list of products')
def step_impl(context):
    assert 'Products' in context.browser.title

@then('I should see the details of the selected product')
def step_impl(context):
    assert 'Details' in context.browser.title