from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from .base import wait

class ListPage(object):
    '''list page object'''

    def __init__(self, test):
        self.test = test

    def start(self):
        '''generic start function'''
        return self.go_home_page()

    def go_home_page(self):
        '''go to home page'''
        self.test.browser.get(self.test.live_server_url)
        return self

    def get_table_rows(self):
        '''get rows from the table'''
        return self.test.browser.find_elements(By.CSS_SELECTOR, '#id_list_table tr')

    def get_error_element(self):
        '''return error element from the page'''
        return self.test.browser.find_element(By.CSS_SELECTOR, '.has-error')

    @wait
    def wait_for_row_in_list_table(self, item_text, item_number):
        row_text = '{}: {}'.format(item_number, item_text)
        rows = self.get_table_rows()
        self.test.assertIn(row_text, [row.text for row in rows])

    @wait
    def check_item_text_is_valid(self):
        '''check item text input box has no error elements'''
        self.test.assertIsNotNone(
            self.test.browser.find_element(By.CSS_SELECTOR, '#id_text:valid')
        )
        return self

    @wait
    def check_item_text_is_invalid(self):
        '''check item text input box has an error element'''
        self.test.assertIsNotNone(
            self.test.browser.find_element(By.CSS_SELECTOR, '#id_text:invalid')
        )
        return self

    @wait
    def check_has_error(self, error_text):
        '''check page has error element with the error_text'''
        self.test.assertEqual(
            error_text,
            self.get_error_element().text
        )
        return self

    @wait
    def check_error_is_displayed(self):
        '''check page has error element which is displayed'''
        self.test.assertTrue(
            self.get_error_element().is_displayed()
        )
        return self

    @wait
    def check_error_is_cleared(self):
        '''check page has no error element displayed'''
        self.test.assertFalse(
            self.get_error_element().is_displayed()
        )
        return self

    @wait
    def check_logged_out(self):
        '''check the user has logged out'''
        self.test.assertEqual(
            self.test.browser.find_elements(By.LINK_TEXT, 'My lists'),
            []
        )
        return self

    @wait
    def check_list_link_present(self, list_name):
        '''check list item is present'''
        self.get_url_by_text(list_name)
        return self

    def get_item_input_box(self):
        '''get input box'''
        return self.test.browser.find_element(By.ID, 'id_text')

    @wait
    def check_url_is_present(self, text):
        '''checks that url with the given text is present'''
        self.test.assertIsNotNone(
            self.get_url_by_text(text)
        )
        return self

    def get_url_by_text(self, text):
        '''get url by link text'''
        return self.test.browser.find_element(By.LINK_TEXT, text)


    def add_list_item(self, item_text):
        '''add an item to the list'''
        new_item_no = len(self.get_table_rows()) + 1
        self.get_item_input_box().send_keys(item_text)
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table(item_text, new_item_no)
        return self

    def try_to_add_list_item(self, item_text):
        '''try add an item to the list, no check'''
        self.get_item_input_box().send_keys(item_text)
        self.get_item_input_box().send_keys(Keys.ENTER)
        return self

    def get_share_box(self):
        '''get field for list sharing'''
        return self.test.browser.find_element(
                By.CSS_SELECTOR, 'input[name="sharee"]'
        )

    def get_shared_with_list(self):
        '''get a list of persons the list is shared with'''
        return self.test.browser.find_elements(
                By.CSS_SELECTOR, '.list-sharee'
        )

    def share_list_with(self, email):
        '''share with other person'''
        self.get_share_box().send_keys(email)
        self.get_share_box().send_keys(Keys.ENTER)
        self.test.wait_for(
            lambda: self.test.AssertIn(
                email,
                [item.text for item in self.get_shared_with_list()]
            )
        )

    def go_to_my_lists_page(self):
        '''go to 'My lists' page'''
        self.get_my_lists_url().click()
        self.test.wait_for(
            lambda: self.test.assertEqual(
                'My lists',
                self.test.browser.find_element(By.TAG_NAME, 'h1').text
            )
        )
        return self

    def logout(self):
        '''return Log out url'''
        self.get_url_by_text('Log out').click()
        return self

    def get_my_lists_url(self):
        '''return url to My lists'''
        return self.get_url_by_text('My lists')


    def get_list_owner(self):
        '''return current list owner'''
        return self.test.browser.find_element(By.ID, 'id_list_owner').text
