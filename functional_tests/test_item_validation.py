#!/usr/bin/env python

from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
import unittest
from .list_page import ListPage

import logging
logger = logging.getLogger(__name__)

class ItemValidationTest(FunctionalTest):
    '''проверка валидации вводимых значений'''

    def test_cannot_add_empty_list_items(self):
        '''тест: нельзя добавлять пустые элементы списка'''
        # Эдит открывает домашнюю страницу и случайно пытается отправить
        # пустой элемент списка. Она нажимает Enter на пустом поле ввода
        list_page = ListPage(self).start()
        list_page.get_item_input_box().send_keys(Keys.ENTER)

        # Браузер перехватывает запрос и не позволяет отправить пустое поле
        list_page.check_item_text_is_invalid()

        # Она начинает набирать текст и ошибка исчезает
        list_page.get_item_input_box().send_keys("Купить молоко")
        list_page.check_item_text_is_valid()

        # Элемент можно сохранить на сервер
        list_page.get_item_input_box().send_keys(Keys.ENTER)
        list_page.wait_for_row_in_list_table('Купить молоко', 1)

        # Как ни странно, Эдит решает отправить второй пустой элемент списка
        list_page.get_item_input_box().send_keys(Keys.ENTER)

        # Браузер опять перехватывает запрос и не позволяет отправить пустое поле
        list_page.check_item_text_is_invalid()

        # И она может его исправить, заполнив поле неким текстом
        list_page.get_item_input_box().send_keys("Заварить чай")

        # ошибка исчезает
        list_page.check_item_text_is_valid()

        # Сохраняет элемент и проверяет список
        list_page.get_item_input_box().send_keys(Keys.ENTER)
        list_page.wait_for_row_in_list_table('Купить молоко', 1)
        list_page.wait_for_row_in_list_table('Заварить чай', 2)

    def test_cannot_add_duplicate_items(self):
        '''test: duplicate items are forbidden'''

        # Эдит открывает новую страницу и начинает новые список
        list_page = ListPage(self).start()

        # can be replaced with list_page.add_list_item()
        list_page.get_item_input_box().send_keys("Купить сапоги")
        list_page.get_item_input_box().send_keys(Keys.ENTER)
        list_page.wait_for_row_in_list_table('Купить сапоги', 1)

        # пытается добавить элемент повторно
        list_page.get_item_input_box().send_keys("Купить сапоги")
        list_page.get_item_input_box().send_keys(Keys.ENTER)

        # и получает сообщение об ошибке
        list_page.check_has_error(
            "You've already got this item in your list"
        )

    def test_error_messages_are_cleared_on_input(self):
        '''test: error message disappears on user input'''
        # Этид начинает список и вызывает ошибку валидации
        list_page = ListPage(self).start()
        ##list_page.get_item_input_box().send_keys("Error message clearning test")
        ##list_page.get_item_input_box().send_keys(Keys.ENTER)
        ##list_page.wait_for_row_in_list_table('Error message clearning test', 1)
        ##list_page.get_item_input_box().send_keys("Error message clearning test")
        ##list_page.get_item_input_box().send_keys(Keys.ENTER)
        list_page.add_list_item("Error message clearning test")
        list_page.try_to_add_list_item("Error message clearning test")

        # и получает сообщение об ошибке
        list_page.check_error_is_displayed()

        # начинает набирать новый элемент в поле ввода
        list_page.get_item_input_box().send_keys("a")

        # и сообщение об ошибке исчезает
        list_page.check_error_is_cleared()
