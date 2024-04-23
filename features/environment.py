import os
from django.conf import settings
from django.test import LiveServerTestCase  # Import LiveServerTestCase instead of TestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Setup Django environment correctly
os.environ['DJANGO_SETTINGS_MODULE'] = 'cc_app.settings'
import django
django.setup()

def before_all(context):
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test_database'
    }

    # Initialize and set up the LiveServerTestCase
    context.live_server = LiveServerTestCase()
    context.live_server.setUpClass()  # Proper setup for live server
    context.test = context.live_server  # Ensure context.test points to the live server instance

    # Set up the WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    context.browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def get_url(context, url_name):
    """
    Helper function to get the absolute URL for a given URL name using Django's reverse function.
    """
    return context.test.live_server_url + reverse(url_name)  # Now it properly uses the live server URL

def before_scenario(context, scenario):
    """
    Setup function to be executed before each scenario.
    """
    context.get_url = get_url  # Attach the get_url function to the context object
    
    # Reinitialize LiveServerTestCase if needed
    if 'django' in scenario.tags:
        context.test_case = LiveServerTestCase()
        context.test_case.setUpClass()
        context.test = context.test_case  # Make sure context.test is correctly updated

    if 'selenium' in scenario.tags:
        # Optionally reinitialize the browser for Selenium-based scenarios
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        context.browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def after_scenario(context, scenario):
    # Handle test case teardown
    if hasattr(context, 'test_case'):
        context.test_case.tearDown()

    # Close the browser if it's a Selenium test
    if 'selenium' in scenario.tags and hasattr(context, 'browser'):
        context.browser.quit()

def after_all(context):
    """
    Clean up and close the browser once all tests are done.
    Also clean up the live server test case.
    """
    if hasattr(context, 'live_server'):
        context.live_server.tearDownClass()  # Properly tear down the live server

    if hasattr(context, 'browser'):
        context.browser.quit()