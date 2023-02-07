from django.test import TestCase
from django.urls import resolve, reverse
from lists.views import home_page
from django.template.loader import render_to_string
from lists.models import Item, List
from lists.forms import (
        ExistingListItemForm, ItemForm,
        EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR
)
from django.utils.html import escape
import unittest
from django.contrib import auth

User = auth.get_user_model()

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

    def test_home_page_uses_item_form(self):
        '''test: home page uses ItemForm for input'''
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)

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

    def test_save_a_POST_request_to_an_existing_list(self):
        '''test: can save a POST request to an existing list'''
        correct_list = List.objects.create()
        wrong_list = List.objects.create()

        self.client.post(
                f'/lists/{correct_list.id}/',
                data={'text': 'A new item for the correct list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for the correct list')
        self.assertEqual(new_item.list, correct_list)

    def test_new_item_POST_redirects_to_correct_list_url(self):
        '''test: POST request redirects to correct list view'''
        correct_list = List.objects.create()

        response = self.client.post(
                f'/lists/{correct_list.id}/',
                data={'text': 'Redirect test for the new item'}
        )

        self.assertRedirects(response, f'/lists/{correct_list.id}/')

    def test_validation_errors_end_up_on_lists_page(self):
        '''test: validation errors are shown on the list page'''
        list_ = List.objects.create()
        response = self.client.post(
                f'/lists/{list_.id}/',
                data={'text': ''}
                )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')
        expected_error = escape(EMPTY_ITEM_ERROR)
        self.assertContains(response, expected_error)
    
    def post_invalid_input(self):
        '''make a post request with invalid data'''
        list_ = List.objects.create()
        return self.client.post(f'/lists/{list_.id}/',
                                data={'text': ''})

    def test_for_invalid_input_nothing_saved_to_db(self):
        '''test: ivalid input doesn't save to database'''
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_renders_list_template(self):
        '''test: invalid input in the existing lists renders lists templates'''
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')

    def test_for_invalid_input_passes_form_to_template(self):
        '''test: invalid input still pass form object to template'''
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ExistingListItemForm)

    def test_for_invalid_input_shows_error_on_the_page(self):
        '''test: invalid input shows error on the page'''
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_displays_item_form(self):
        '''test: list view shows item form'''
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertIsInstance(response.context['form'], ExistingListItemForm)
        self.assertContains(response, 'name="text"')

    def test_duplicate_item_validation_errors_end_up_on_lists_page(self):
        '''test: duplicate item validation error goes to lists page'''
        list_ = List.objects.create()
        item = Item.objects.create(list=list_, text='dup_test')
        response = self.client.post(
                f'/lists/{list_.id}/',
                data={'text': 'dup_test'}
        )
        expected_error = escape(DUPLICATE_ITEM_ERROR)
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, 'list.html')
        self.assertEqual(Item.objects.all().count(), 1)

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
        response = self.client.post('/lists/new', data={'text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_get_redirect_after_POST_request(self):
        '''test: POST request return redirect to home page'''
        response = self.client.post('/lists/new', data={'text': 'A new list item'})
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')

    def test_for_invalid_input_renders_home_template(self):
        '''test: invalid input shows page on home template'''
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_validation_errors_are_shown_on_the_page(self):
        '''test: error about invalid input shown on the page'''
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_for_invalid_input_to_new_list_passes_form_to_template(self):
        '''test: invalid input for new list pass form object to template'''
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_for_invalid_input_to_existing_list_passes_form_to_template(self):
        '''test: invalid input for existing list pass form object to template'''
        list_ = List.objects.create()
        response = self.client.post(
                f'/lists/{list_.id}/',
                data={'text': ''}
        )
        self.assertIsInstance(response.context['form'], ExistingListItemForm)

    def test_invalid_list_items_arent_saved(self):
        '''test: invalid items arent saved at all'''

        self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)

class NewListItemTest(TestCase):
    '''test adding item to existing list'''
    pass


class UserListsTest(TestCase):
    '''test for user's own lists'''

    def test_user_lists_url_renders_user_lists_template(self):
        '''test: use correct template'''
        User.objects.create(email='a@b.c')
        response = self.client.get(reverse('user_lists', args=['a@b.c']))
        self.assertTemplateUsed(response, 'user_lists.html')

    def test_passes_correct_owner_to_template(self):
        '''test: we pass correct owner to render'''
        User.objects.create(email='some@user')
        email = 'correct@user.com'
        correct_user = User.objects.create(email=email)
        response = self.client.get(reverse('user_lists', args=[email]))
        self.assertEqual(response.context['owner'], correct_user)

    def test_list_owner_is_saved_if_user_is_authenticated(self):
        '''test: list owner is saved for authenticated users'''
        email = 'correct@user.com'
        user = User.objects.create(email=email)
        self.client.force_login(user)
        response = self.client.post(reverse('new_list'), data={'text': 'A new list item'})
        list_ = List.objects.first()
        self.assertEqual(list_.owner, user)


