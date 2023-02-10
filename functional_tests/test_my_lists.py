from django.contrib.sessions.backends.db import SessionStore
from selenium.webdriver.common.by import By
from .base import FunctionalTest

import logging
logger = logging.getLogger(__name__)

class MyListsTest(FunctionalTest):
    '''test users own todo lists'''

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        '''test: lists for the authenticated users are saved as my_lists'''

        # Эдит является зарегистриованным пользователем
        email = 'edith@example.com'
        self.create_pre_authenticated_session_by_session(email)
        ##self.create_pre_authenticated_session_by_token(email) # works OK

        # она подключается к системе и начинает новый список
        self.browser.get(self.live_server_url)
        self.add_list_item('Снять шторы')
        self.add_list_item('И постирать их')
        first_list_url = self.browser.current_url

        # Она замечает ссылку "My lists" и решает проверить, что там
        self.browser.find_element(By.LINK_TEXT, 'My lists').click()

        # И видит там свой список дел, названный по первому пункту
        self.wait_for(
            lambda: self.browser.find_element(By.LINK_TEXT, 'Снять шторы')
        )

        # Кликает в него и попадает на страничку своего списка дел
        self.browser.find_element(By.LINK_TEXT, 'Снять шторы').click()
        self.wait_for(
            lambda: self.assertEqual(first_list_url, self.browser.current_url)
        )

        # она решает создать еще один список
        self.browser.get(self.live_server_url)
        self.add_list_item('Подмести пол')
        second_list_url = self.browser.current_url

        # Она замечает ссылку "My lists" и решает проверить, что там
        self.browser.find_element(By.LINK_TEXT, 'My lists').click()

        # И проверяет, что новый список отображается в "My lists"
        self.browser.find_element(By.LINK_TEXT, 'My lists').click()
        self.wait_for(
            lambda: self.browser.find_element(By.LINK_TEXT, 'Подмести пол')
        )
        self.browser.find_element(By.LINK_TEXT, 'Подмести пол').click()
        self.wait_for(
            lambda: self.assertEqual(second_list_url, self.browser.current_url)
        )

        # Она выходит из системы и опция "My lists" пропадает
        self.browser.find_element(By.LINK_TEXT, 'Log out').click()
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_elements(By.LINK_TEXT, 'My lists'),
                []
            )
        )
