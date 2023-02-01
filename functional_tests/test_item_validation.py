#!/usr/bin/env python

from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
import unittest

class ItemValidationTest(FunctionalTest):
    '''проверка валидации вводимых значений'''

    def get_error_element(self):
        '''return error element from the page'''
        return self.browser.find_element(By.CSS_SELECTOR, '.has-error')

    def test_cannot_add_empty_list_items(self):
        '''тест: нельзя добавлять пустые элементы списка'''
        # Эдит открывает домашнюю страницу и случайно пытается отправить
        # пустой элемент списка. Она нажимает Enter на пустом поле ввода
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        # Браузер перехватывает запрос и не позволяет отправить пустое поле
        self.wait_for(lambda: self.assertIsNotNone(
            self.browser.find_element(By.CSS_SELECTOR, '#id_text:invalid')
        ))

        # Она начинает набирать текст и ошибка исчезает
        self.get_item_input_box().send_keys("Купить молоко")
        self.wait_for(lambda: self.assertIsNotNone(
            self.browser.find_element(By.CSS_SELECTOR, '#id_text:valid')
        ))

        # Элемент можно сохранить на сервер
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить молоко')

        # Как ни странно, Эдит решает отправить второй пустой элемент списка
        self.get_item_input_box().send_keys(Keys.ENTER)

        # Браузер опять перехватывает запрос и не позволяет отправить пустое поле
        self.wait_for(lambda: self.assertIsNotNone(
            self.browser.find_element(By.CSS_SELECTOR, '#id_text:invalid')
        ))

        # И она может его исправить, заполнив поле неким текстом
        self.get_item_input_box().send_keys("Заварить чай")

        # и ошибка исчезает
        self.wait_for(lambda: self.assertIsNotNone(
            self.browser.find_element(By.CSS_SELECTOR, '#id_text:valid')
        ))

        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить молоко')
        self.wait_for_row_in_list_table('2: Заварить чай')

    def test_cannot_add_duplicate_items(self):
        '''test: duplicate items are forbidden'''

        # Эдит открывает новую страницу и начинает новые список
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys("Купить сапоги")
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить сапоги')

        # пытается добавить элемент повторно
        self.get_item_input_box().send_keys("Купить сапоги")
        self.get_item_input_box().send_keys(Keys.ENTER)

        # и получает сообщение об ошибке
        self.wait_for(lambda: self.assertEqual(
            self.get_error_element().text,
            "You've already got this item in your list"
        ))

    def test_error_messages_are_cleared_on_input(self):
        '''test: error message disappears on user input'''
        # Этид начинает список и вызывает ошибку валидации
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys("Error message clearning test")
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Error message clearning test')
        self.get_item_input_box().send_keys("Error message clearning test")
        self.get_item_input_box().send_keys(Keys.ENTER)

        # и получает сообщение об ошибке
        self.wait_for(lambda: self.assertTrue(
            self.get_error_element().is_displayed()
        ))

        # начинает набирать новый элемент в поле ввода
        self.get_item_input_box().send_keys("a")

        # и сообщение об ошибке исчезает
        self.wait_for(lambda: self.assertFalse(
            self.get_error_element().is_displayed()
        ))
