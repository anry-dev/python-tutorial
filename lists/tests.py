from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string

# Create your tests here.
class HomePageTest(TestCase):
    '''test for correct home page'''

    def test_root_url_resolves_to_home_page_views(self):
        '''тест: корневой url преобразуется в представление домашней страницы'''
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_root_url_returns_correct_html(self):
        '''test: home page must return correct html'''

        response = self.client.get('/')

        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>To-Do lists</title>', html)
        self.assertTrue(html.strip().endswith('</html>'))

        self.assertTemplateUsed(response, 'home.html')
