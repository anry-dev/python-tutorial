from django.core import mail
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import re
# pop3 client
import os
import time
import poplib

from .base import FunctionalTest

TEST_EMAIL = 'supertlist@lab.rt.ru'
REAL_EMAIL = 'django-test@lab.rt.ru'
SUBJECT = 'Your login link for Superlists'

import logging
logger = logging.getLogger(__name__)
logger.debug(f'module: {__name__}')

class LoginTest(FunctionalTest):
    '''test form user registrations'''

    def wait_for_mail(self, test_email, subject):
        '''wait for email'''
        if not self.staging_server:
            email = mail.outbox[0]
            self.assertIn(test_email, email.to)
            self.assertIn(subject, email.subject)
            return email.body

        email_id = None
        start = time.time()
        inbox = poplib.POP3_SSL('mail.lab.rt.ru')
        try:
            inbox.user(test_email)
            inbox.pass_(os.environ['MAIL_PASSWORD'])
            while time.time() - start < 60:
                # get 10 the most new messages
                count, _ = inbox.stat()
                for i in reversed(range(max(1, count - 10), count + 1)):
                    _, lines, __ = inbox.retr(i)
                    lines = [l.decode('utf8') for l in lines]
                    logger.debug(lines)
                    if f'Subject: {subject}' in lines:
                        email_id = i
                        body = '\n'.join(lines)
                        return body
                    time.sleep(5)
        finally:
            if email_id:
                inbox.dele(email_id)
            inbox.quit()

    def test_can_get_login_link_via_email(self):
        '''test: can get login link via email'''

        if self.staging_server:
            test_email = REAL_EMAIL
        else:
            test_email = TEST_EMAIL

        # Эдит заходит на сайт впервые
        # и замечает раздел "Войти" - ???? нет теста !!!
        # ей предлагаю ввести адрес email, что она и делает
        self.browser.get(self.live_server_url)
        self.browser.find_element(By.NAME, 'email').send_keys(test_email)
        self.browser.find_element(By.NAME, 'email').send_keys(Keys.ENTER)

        # появляется сообщение, что письмо отправлено
        self.wait_for(lambda: self.assertIn(
            'Check your mail',
            self.browser.find_element(By.TAG_NAME, 'body').text
        ))

        # Она проверяет почту
        # И находит сообщение с правильным заголовком
        body = self.wait_for_mail(test_email, SUBJECT)

        # Письмо содержит ссылку для логина
        self.assertIn('Use this link to log in', body)
        url_search = re.search(r'http://.+/.+$', body)
        if not url_search:
            self.fail(f'Could not find url in email body:\n{body}')

        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)
        logger.debug(f'Got url: {url}')

        # Этит переходит по ссылке
        self.browser.get(url)

        # И видит, что она зарегистрирована в системе
        self.wait_to_be_logged_in(email=test_email)

        # После чего она пытается выйти из системы
        self.browser.find_element(By.LINK_TEXT, 'Log out').click()

        # И проверяет, что она действительно вышла из системы
        self.wait_to_be_logged_out(email=test_email)
