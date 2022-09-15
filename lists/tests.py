from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.template.loader import render_to_string
from lists.models import Item

# Create your tests here.
class HomePageTest(TestCase):
    '''test for correct home page'''

    def test_uses_home_template(self):
        '''test: home page must return correct html'''
        response = self.client.get('/')
        html = response.content.decode('utf8')
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

class ListViewTest(TestCase):
    '''List view tests'''

    def test_uses_list_template(self):
        '''test: using list template'''
        response = self.client.get('/lists/the_uniq_url_in_the_world/')
        html = response.content.decode('utf8')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_list_items(self):
        '''test: home page displays all list elements'''
        Item.objects.create(text='item 1')
        Item.objects.create(text='item 2')

        response = self.client.get('/lists/the_uniq_url_in_the_world/')

        self.assertContains(response, 'item 1')
        self.assertContains(response, 'item 2')

class NewViewTest(TestCase):
    '''test creating a new list'''

    def test_get_request_doesn_fail(self):
        '''test: get request doesnt fail'''
        response = self.client.get('/lists/new')
        self.assertEqual(response.status_code, 302)

    def test_url_with_slash_not_works(self):
        '''test: url with ending slash doesnt work'''
        response = self.client.get('/lists/new/')
        self.assertEqual(response.status_code, 404)

    def test_can_save_a_POST_request(self):
        '''test: save a POST request'''
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_get_redirect_after_POST_request(self):
        '''test: POST request return redirect to home page'''
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertRedirects(response, '/lists/the_uniq_url_in_the_world/')

