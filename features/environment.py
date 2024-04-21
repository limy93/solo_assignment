import os
from django.conf import settings
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
        
    # Set up the WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    context.browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def get_url(context, url_name):
    """
    Helper function to get the absolute URL for a given URL name using Django's reverse function.
    """
    return context.test.live_server_url + reverse(url_name)

def before_scenario(context, scenario):
    """
    Setup function to be executed before each scenario.
    """
    # Attach the get_url function to the context object
    context.get_url = get_url
    
    if 'selenium' in scenario.tags:
        from selenium import webdriver
        context.browser = webdriver.Chrome()  

def after_scenario(context, scenario):

    if 'selenium' in scenario.tags and hasattr(context, 'browser'):
        context.browser.quit()

def after_all(context):
    # Clean up and close the browser once tests are done
    context.browser.quit()