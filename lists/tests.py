from django.test import TestCase
from django.urls import resolve
from lists.views import home_page

# Create your tests here.
class HomePageTest(TestCase):
    '''test for correct home page'''

    def test_root_url_resolves_to_home_page_views(self):
        '''тест: корневой url преобразуется в представление домашней страницы'''
        found = resolve('/')
        self.assertEqual(found.func, home_page)
