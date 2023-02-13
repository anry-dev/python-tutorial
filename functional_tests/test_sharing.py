from .base import FunctionalTest
from selenium.webdriver.common.by import By
from .list_page import ListPage
from .my_lists_page import MyListsPage

import logging
logger = logging.getLogger(__name__)

def quit_if_possible(browser):
    try: browser.quit()
    except: pass

class SharingTest(FunctionalTest):
    '''test list sharing'''

    def test_can_share_a_list_with_another_user(self):
        '''test: list can be shared with other users'''

        # Эдит является зарегистриованным пользователем
        self.browser.set_window_size(500, 600)
        self.browser.set_window_position(0, 0)
        self.create_pre_authenticated_session('edith@example.com')
        edith_browser = self.browser
        self.addCleanup(lambda: quit_if_possible(edith_browser))

        # Ее друг Tom тоже пользователь суперсписков
        tom_browser = FunctionalTest.runBrowser()
        self.addCleanup(lambda: quit_if_possible(tom_browser))
        self.browser = tom_browser
        self.browser.set_window_size(500, 600)
        self.browser.set_window_position(520, 0)
        self.create_pre_authenticated_session('tom@example.com')

        # Эдит открывает домашнюю страницу и начинает новый список
        self.browser = edith_browser
        list_page = ListPage(self).start().add_list_item('Get help')

        # Она замечает опцию "Поледиться ..."
        share_box = list_page.get_share_box() # self.browser.find_element(By.CSS_SELECTOR, 'input[name="sharee"]')
        self.assertEqual(
                share_box.get_attribute('placeholder'),
                'your-friend@example.com'
        )

        # Она делится своим списком с Tom
        # Страница обновляется и сообщает
        # что используется совместно с пользователем Tom
        list_page.share_list_with('tom@example.com')

        # Tom переходит к своим спискам доступа
        self.browser = tom_browser
        ListPage(self).start()
        list_page.go_to_my_lists_page()

        # И видит на ней список от Эдит
        # И переходит на него
        self.browser.find_element(By.LINK_TEXT, 'Get help').click()
        
        # На странице, которую он видет, говорится,
        # что это список от Эдит
        self.wait_for( lambda: self.assertEqual(
            list_page.get_list_owner(),
            'edith@example.com'
        ))

        # Он добавляет новый элемент в список
        list_page.add_list_item('Привет, Эдит!')
        
        # Когда Эдит обновляет страницу она видит запись от Тома
        self.browser = edith_browser
        self.browser.refresh()
        list_page.wait_for_row_in_list_table('Привет, Эдит!', 2)

