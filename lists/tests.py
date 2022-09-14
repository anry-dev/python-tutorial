from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.template.loader import render_to_string
from lists.models import Item

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
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        '''test: home pages save a POST request'''

        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertIn('A new list item', response.content.decode())
        self.assertTemplateUsed(response, 'home.html')

class ItemModelTest(TestCase):
    '''List elements model tests'''

    def test_saving_and_retrieving_items(self):
        '''test to save and retrieve an item'''

        first_item = Item()
        first_item.text = 'Just the first item!'
        first_item.save()

        second_item = Item()
        second_item.text = 'The second item.'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'Just the first item!')
        self.assertEqual(second_saved_item.text, 'The second item.')

