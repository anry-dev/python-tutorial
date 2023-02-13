from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from .base import wait
from .list_page import ListPage

class MyListsPage(ListPage):
    '''list page object'''

    def start(self):
        '''generict full startup'''
        super.start()
        return self.go_to_my_lists_page()

    def go_to(self):
        '''shortcut to go_to_my_lists_page'''
        return self.go_to_my_lists_page()

    def go_to_my_lists_page(self):
        '''go to 'My Lists' page'''
        self.test.browser.find_element(By.LINK_TEXT, 'My lists').click()
        self.test.wait_for(
            lambda: self.test.assertEqual(
                'My lists',
                self.test.browser.find_element(By.TAG_NAME, 'h1').text
            )
        )
        return self
