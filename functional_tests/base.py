#!/usr/bin/env python

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, NoSuchElementException
import time
import unittest
import os
from .server_tools import reset_database

import logging
logger = logging.getLogger(__name__)

# screen dumps config
from datetime import datetime
from pathlib import Path

# create_pre_auth_session
from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from .server_tools import create_session_on_server, create_token_on_server
from .management.commands.create_session import create_pre_authenticated_session
from .management.commands.create_token import create_auth_token
User = get_user_model()

# Path(__file__) - full path to base.py
SCREEN_DUMP_LOCATION = Path(__file__).resolve().parent.joinpath('screendumps')
#SCREEN_DUMP_LOCATION = Path(__file__).resolve().parent.parent.parent.joinpath('screendumps')

MAX_WAIT = 10


def wait(fn):
        '''wait decorator'''
        def modified_fn(*args, **kwargs):
            start_time = time.time()
            while True:
                try:
                    return fn(*args, **kwargs)
                except (AssertionError, WebDriverException) as e:
                    if time.time() - start_time > MAX_WAIT:
                        raise e
                    time.sleep(0.5)
        return modified_fn

def waitt(wait_time = MAX_WAIT, step = 0.5):
        '''wait decorator with args
           must be placed as:
           @waitt(args)
        '''
        def decorator(fn):
            def wrapper(*args, **kwargs):
                start_time = time.time()
                while True:
                    try:
                        return fn(*args, **kwargs)
                    except (AssertionError, WebDriverException) as e:
                        if time.time() - start_time > MAX_WAIT:
                            raise e
                        time.sleep(step)
            return wrapper 
        return decorator


class FunctionalTest(StaticLiveServerTestCase):
    '''функциональный тест - обертка'''

    def runBrowser(opts=None):
        '''run Firefix with preset size'''
        if opts is None:
            opts = webdriver.FirefoxOptions()
            opts.add_argument("--width=800")
            opts.add_argument("--height=600")
        return webdriver.Firefox(options=opts)

    def setUp(self):
        '''setup'''
        #self.browser = webdriver.Firefox()
        self.browser = FunctionalTest.runBrowser()
        self.staging_server = os.environ.get('STAGING_SERVER')
        if self.staging_server:
            print('Setting staging server to: %s' % (self.staging_server,))
            self.live_server_url = 'http://' + self.staging_server
            reset_database(self.staging_server)

    def tearDown(self):
        '''shutdown'''
        #if self._test_has_failed():
        if self._need_dumps():
            if not SCREEN_DUMP_LOCATION.exists():
                SCREEN_DUMP_LOCATION.mkdir()
            for ix, handle in enumerate(self.browser.window_handles):
                self._windowid = ix
                self.browser.switch_to.window(handle)
                self.take_screenshot()
                self.dump_html()

        self.browser.quit()
        super().tearDown()

    def _need_dumps(self):
        '''check do we need to save dumps'''
        return self._test_has_failed() and os.environ.get('SUPERLIST_DUMP')

    def _test_has_failed(self):
        '''check that test has failed'''
        # uhh
        return any(error for (method, error) in self._outcome.errors)

    def _get_filename(self):
        '''make filename for data saving'''
        timestamp = datetime.now().isoformat().replace(':', '.')[:19]
        return '{folder}/{classname}.{method}-window{windowid}-{timestamp}'.\
            format(
                folder=str(SCREEN_DUMP_LOCATION),
                classname=self.__class__.__name__,
                method=self._testMethodName,
                windowid=self._windowid,
                timestamp=timestamp,
            )

    def take_screenshot(self):
        '''save current window screenshot to SCREEN_DUMP_LOCATION'''
        filename = self._get_filename() + '.png'
        print(f'screenshotting to {filename}')
        self.browser.get_screenshot_as_file(filename)

    def dump_html(self):
        '''save current page source to SCREEN_DUMP_LOCATION'''
        filename = self._get_filename() + '.html'
        print(f'dumping page HTML to {filename}')
        with open(filename, 'w') as f:
            f.write(self.browser.page_source)

    @wait
    def wait_for_row_in_list_table(self, row_text):
        '''wait for a row to present in the list table'''
        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertIn(row_text, [row.text for row in rows])

    @wait
    def wait_for(self, fn):
        return fn()

    def get_item_input_box(self):
        '''return input field for the form'''
        return self.browser.find_element(By.ID, 'id_text')

    def add_list_item(self, item_text):
        '''add new list item'''
        num_rows = len(self.browser.find_elements(By.CSS_SELECTOR, '#id_list_table tr'))
        self.get_item_input_box().send_keys(item_text)
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table(f'{num_rows + 1}: {item_text}')

    @wait
    def wait_to_be_logged_in(self, email):
        '''waiting for user with email to be logged in'''
        self.browser.find_element(By.LINK_TEXT, 'Log out')
        navbar = self.browser.find_element(By.CSS_SELECTOR, '.navbar')
        self.assertIn(email, navbar.text)

    @wait
    def wait_to_be_logged_out(self, email):
        '''waiting for user to log out'''
        self.browser.find_element(By.NAME, 'email')
        navbar = self.browser.find_element(By.CSS_SELECTOR, '.navbar')
        self.assertNotIn(email, navbar.text)


    def create_pre_authenticated_session_by_token(self, email):
        '''make web sessions authenticated on the server'''
        if self.staging_server:
            token = create_token_on_server(self.staging_server, email)
            #self.browser.get(url)
        else:
            token = create_auth_token(email)

        url = f'{self.live_server_url}/accounts/login?token={token}'
        self.browser.get(url)

    def create_pre_authenticated_session_by_session(self, email):
        '''make web sessions authenticated on the server'''
        if self.staging_server:
            session_key = create_session_on_server(self.staging_server, email)
        else:
            session_key = create_pre_authenticated_session(email)

        # set cookies for the browser
        # page 404 loads faster then other
        self.browser.get(self.live_server_url + '/404_no_such_url/')
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session_key,
            path='/',
        ))

    def create_pre_authenticated_session(self, email):
        '''create session shortcut'''
        return self.create_pre_authenticated_session_by_session(email)
