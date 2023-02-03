from django.core import mail
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import re

from .base import FunctionalTest

TEST_EMAIL = 'supertlist@lab.rt.ru'
SUBJECT = 'Your login link for Superlists'

import logging
logger = logging.getLogger(__name__)
logger.debug(f'module: {__name__}')

class LoginTest(FunctionalTest):
    '''test form user registrations'''

    def test_can_get_login_link_via_email(self):
        '''test: can get login link via email'''

        # Эдит заходит на сайт впервые
        # и замечает раздел "Войти" - ???? нет теста !!!
        # ей предлагаю ввести адрес email, что она и делает
        self.browser.get(self.live_server_url)
        self.browser.find_element(By.NAME, 'email').send_keys(TEST_EMAIL)
        self.browser.find_element(By.NAME, 'email').send_keys(Keys.ENTER)

        # появляется сообщение, что письмо отправлено
        self.wait_for(lambda: self.assertIn(
            'Check your mail',
            self.browser.find_element(By.TAG_NAME, 'body').text
        ))

        # Она проверяет почту
        # И находит сообщение с правильным заголовком
        email = mail.outbox[0]      # test feature !!!
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(SUBJECT, email.subject)

        # Письмо содержит ссылку для логина
        self.assertIn('Use this link to log in', email.body)
        url_search = re.search(r'http://.+/.+$', email.body)
        if not url_search:
            self.fail(f'Could not find url in email body:\n{email.body}')

        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)
        logger.debug(f'Got url: {url}')

        # Этит переходит по ссылке
        self.browser.get(url)

        # И видит, что она зарегистрирована в системе
        self.wait_for(
                lambda: self.browser.find_element(By.LINK_TEXT, 'Log out')
        )

        # И видит свой email
        navbar = self.browser.find_element(By.CSS_SELECTOR, '.navbar')
        self.assertIn(TEST_EMAIL, navbar.text)

        # После чего она пытается выйти из системы
        self.browser.find_element(By.LINK_TEXT, 'Log out').click()

        # И проверяет, что она действительно вышла из системы
        with self.assertRaises(NoSuchElementException):
            self.browser.find_element(By.LINK_TEXT, 'Log out')

        navbar = self.browser.find_element(By.CSS_SELECTOR, '.navbar')
        self.assertNotIn(TEST_EMAIL, navbar.text)
