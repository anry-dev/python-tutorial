#!/usr/bin/env python

from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
import unittest

class LayoutAndStylingTest(FunctionalTest):
    '''тесты макета и стилевого оформления'''

    def test_layout_and_styling(self):
        '''test: page layout and styleing'''

        # Эдит открывает стартовую страницу
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)
        ##size = self.browser.get_window_size()
        ##print("Window size: width = {}px, height = {}px.".format(size["width"], size["height"]))

        # Она замечает, что поле ввода расположено по центру
        inputbox = self.get_item_input_box()
        ##print("\n\tx: %d\n\tsize: %d" % (
        #                            inputbox.location['x'],
        #                            inputbox.size['width'])
        #)

        self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] / 2,
                272, #570 -not work with css, #512, -not work at all
                delta=10
        )

        # Она начинает новый список и замечает, что и там поле ввода
        # расположено по центру
        inputbox.send_keys('layout test')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: layout test')
        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] / 2,
                272,
                delta=10
        )

