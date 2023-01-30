from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.template.loader import render_to_string
from lists.models import Item, List
from django.utils.html import escape

# Create your tests here.
class HomePageTest(TestCase):
    '''test for correct home page'''

    def test_root_uses_home_template(self):
        '''test: root home page must return correct html'''
        response = self.client.get('/')
        html = response.content.decode('utf8')
        self.assertTemplateUsed(response, 'home.html')

    def test_lists_uses_home_template(self):
        '''test: lists home page must return correct html'''
        response = self.client.get('/lists/')
        html = response.content.decode('utf8')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

class ListViewTest(TestCase):
    '''List view tests'''

    def test_uses_list_template(self):
        '''test: using list template'''
        tmp_list = List.objects.create()
        response = self.client.get(f'/lists/{tmp_list.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_passes_list_id_in_response(self):
        '''test: list_id is returned in response'''
        correct_list = List.objects.create()
        other_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)

    def test_displays_all_items_for_the_given_list(self):
        '''test: list page displays all list elements for the given list'''
        correct_list = List.objects.create()
        Item.objects.create(text='correct item 1', list=correct_list)
        Item.objects.create(text='correct item 2', list=correct_list)

        wrong_list = List.objects.create()
        Item.objects.create(text='wrong item 1', list=wrong_list)
        Item.objects.create(text='wrong item 2', list=wrong_list)

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response, 'correct item 1')
        self.assertContains(response, 'correct item 2')
        self.assertNotContains(response, 'wrong item 1')
        self.assertNotContains(response, 'wrong item 2')

class NewListTest(TestCase):
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
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        '''test: validation errors are sent to home page template'''

        response = self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)

    def test_invalid_list_items_arent_saved(self):
        '''test: invalid items arent saved at all'''

        self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)

class NewListItemTest(TestCase):
    '''test adding item to existing list'''

    def test_save_a_POST_request_to_an_existing_list(self):
        '''test: can save a POST request to an existing list'''
        correct_list = List.objects.create()
        wrong_list = List.objects.create()

        self.client.post(
                f'/lists/{correct_list.id}/add_item',
                data={'item_text': 'A new item for the correct list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for the correct list')
        self.assertEqual(new_item.list, correct_list)

    def test_new_item_POST_redirects_to_correct_list_url(self):
        '''test: POST request redirects to correct list view'''
        correct_list = List.objects.create()

        response = self.client.post(
                f'/lists/{correct_list.id}/add_item',
                data={'item_text': 'Redirect test for the new item'}
        )

        self.assertRedirects(response, f'/lists/{correct_list.id}/')
