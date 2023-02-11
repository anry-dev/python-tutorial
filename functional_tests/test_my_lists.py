from django.contrib.sessions.backends.db import SessionStore
from .base import FunctionalTest
from .list_page import ListPage

import logging
logger = logging.getLogger(__name__)

class MyListsTest(FunctionalTest):
    '''test users own todo lists'''

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        '''test: lists for the authenticated users are saved as my_lists'''

        # Эдит является зарегистриованным пользователем
        email = 'edith@example.com'
        self.create_pre_authenticated_session_by_session(email)

        # она подключается к системе и начинает новый список
        list_page = ListPage(self).start()
        list_page.add_list_item('Снять шторы').add_list_item('И постирать их')
        first_list_url = self.browser.current_url

        # Она замечает ссылку "My lists" и решает проверить, что там
        list_page.go_to_my_lists_page()

        # И видит там свой список дел, названный по первому пункту
        list_page.check_list_link_present('Снять шторы')

        # Кликает в него и попадает на страничку своего списка дел
        list_page.get_url_by_text('Снять шторы').click()
        self.wait_for(
            lambda: self.assertEqual(first_list_url, self.browser.current_url)
        )

        # она решает создать еще один список
        list_page.start().add_list_item('Подмести пол')
        second_list_url = self.browser.current_url

        # Она переходит по ссылке "My lists"
        list_page.go_to_my_lists_page()

        # и проверяет, что новый список отображается в "My lists"
        list_page.check_list_link_present('Подмести пол')

        # кликает на него и попадает на вторую страничку
        list_page.get_url_by_text('Подмести пол').click()
        self.wait_for(
            lambda: self.assertEqual(second_list_url, self.browser.current_url)
        )

        # Она выходит из системы и опция "My lists" пропадает
        list_page.logout().check_logged_out()
