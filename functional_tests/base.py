#!/usr/bin/env python

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
import time
import unittest
import os
from .server_tools import reset_database

MAX_WAIT = 10

class FunctionalTest(StaticLiveServerTestCase):
    '''функциональный тест - обертка'''

    def setUp(self):
        '''setup'''
        self.browser = webdriver.Firefox()
        self.staging_server = os.environ.get('STAGING_SERVER')
        if self.staging_server:
            print('Setting staging server to: %s' % (self.staging_server,))
            self.live_server_url = 'http://' + self.staging_server
            reset_database(self.staging_server)

    def tearDown(self):
        '''shutdown'''
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        '''wait for a row to present in the list table'''
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID, 'id_list_table')
                rows = table.find_elements(By.TAG_NAME, 'tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

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


    @wait
    def wait_for(self, fn):
        return fn()

    def get_item_input_box(self):
        '''return input field for the form'''
        return self.browser.find_element(By.ID, 'id_text')

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
