from behave import given, when, then
from selenium.webdriver.common.by import By

@given('I am on the home page')
def step_impl(context):
    context.browser.get('http://127.0.0.1:8000/')   # Make sure this URL is correct for the local development environment

@when('I click on the "Browse EcoCredits" button')
def step_impl(context):
    ecocredits_button = context.browser.find_element(By.ID, "browse-button")
    ecocredits_button.click()

@when('I click on the "Learn More" button')
def step_impl(context):
    about_button = context.browser.find_element(By.ID, "about-button")
    about_button.click()

@when('I click on the "View Details" button')
def step_impl(context):
    impact_button = context.browser.find_element(By.ID, "impact-button")
    impact_button.click()

@when('I click on the "Register Now" button')
def step_impl(context):
    register_button = context.browser.find_element(By.ID, "register-button")
    register_button.click()

@then('I should see the page title "{title}"')
def step_impl(context, title):
    assert title in context.browser.title

@then('I should be redirected to the Products page')
def step_impl(context):
    assert "Products" in context.browser.title   # Adjust this title to match the countries list page title

@then('I should be redirected to the About page')
def step_impl(context):
    assert "About" in context.browser.title

@then('I should be redirected to the Impact page')
def step_impl(context):
    assert "Impact" in context.browser.title

@then('I should be redirected to the Register page')
def step_impl(context):
    assert "Register" in context.browser.title