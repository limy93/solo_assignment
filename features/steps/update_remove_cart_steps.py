from behave import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@given('I am on the Cart page')
def step_impl(context):
    context.browser.get('http://127.0.0.1:8000/cart/')

@when('I change the quantity of a product')
def step_impl(context):
    # Assuming '1' is the ID attribute value for the quantity input field of the product
    quantity_input = WebDriverWait(context.browser, 10).until(
        EC.visibility_of_element_located((By.ID, 'quantity-1'))
    )
    quantity_input.clear()
    quantity_input.send_keys('2')

@when('I click the "Update" button')
def step_impl(context):
    update_button = WebDriverWait(context.browser, 10).until(
        EC.element_to_be_clickable((By.NAME, 'update'))
    )
    update_button.click()

@then('I should see the cart updated with the new quantity')
def step_impl(context):
    assert context.browser.is_text_present('2 items')

@when('I click the "Remove" button for a product')
def step_impl(context):
    remove_button = WebDriverWait(context.browser, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, 'Remove'))
    )
    remove_button.click()

@then('I should see that the product is no longer in the cart')
def step_impl(context):
    assert context.browser.is_text_not_present('Product Name')