import os
from django.conf import settings
from django.test import LiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# Setup Django environment correctly
os.environ['DJANGO_SETTINGS_MODULE'] = 'cc_app.settings'
import django
django.setup()

def before_all(context):
    # Configure test database
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }

    # Initialize and set up the LiveServerTestCase
    context.live_server = LiveServerTestCase()
    context.live_server.setUpClass()
    context.test = context.live_server

    # Set up the WebDriver
    options = Options()
    options.add_argument('--headless')
    context.browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def before_scenario(context, scenario):
    """
    Setup function to be executed before each scenario.
    Resets the browser to ensure clean state, including cookies and session data.
    """
    if 'django' in scenario.tags:
        # Reinitialize LiveServerTestCase to ensure a clean state
        context.live_server = LiveServerTestCase()
        context.live_server.setUpClass()
        context.test = context.live_server
    
    # Ensure the browser is reinitialized for every scenario, not just those tagged with 'selenium'
    options = Options()
    options.add_argument('--headless')
    # Close existing browser session if it exists
    if hasattr(context, 'browser'):
        context.browser.quit()
    context.browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    context.browser.delete_all_cookies()   # Clear all cookies at the start of each scenario

def get_url(context, url_name):
    """
    Helper function to get the absolute URL for a given URL name using Django's reverse function.
    """
    return context.test.live_server_url + reverse(url_name)

def after_scenario(context, scenario):
    """
    Clean up after each scenario.
    """
    if 'selenium' in scenario.tags and hasattr(context, 'browser'):
        context.browser.quit()

    if 'django' in scenario.tags and hasattr(context, 'live_server'):
        context.live_server.tearDownClass()

def after_all(context):
    """
    Final cleanup after all tests have run.
    """
    if hasattr(context, 'browser'):
        context.browser.quit()
    if hasattr(context, 'live_server'):
        context.live_server.tearDownClass()