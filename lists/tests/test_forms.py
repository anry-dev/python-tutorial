from django.test import TestCase
from lists.forms import (
        EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR,
        ItemForm, ExistingListItemForm, NewListForm
)

import unittest
from unittest.mock import patch, Mock
from lists.models import Item, List

class ItemFormTest(TestCase):
    '''testing forms for elements lists'''

    def test_form_item_input_has_placeholder_and_css_classes(self):
        '''test: form input field has placeholder and css-class attributes'''
        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_items(self):
        '''test: form validations against empty value'''
        form = ItemForm(data={'text': ''})
        #form.save()
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])


class ExistingListItemFormTest(TestCase):
    '''testing ExistingListItermForm methods'''

    def test_form_contains_placeholder(self):
        '''test: form shows placeholder'''
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_)
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())

    def test_form_validation_for_blank_items(self):
        '''test: blank items validation'''
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_, data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])

    def test_form_validation_for_duplicate_items(self):
        '''test: duplicate items validation'''
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='dup1')
        form = ExistingListItemForm(for_list=list_, data={'text': 'dup1'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [DUPLICATE_ITEM_ERROR])

    def test_form_save(self):
        '''test: form.save works correctly'''
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_, data={'text': 'form.save'})
        item = form.save()
        self.assertEqual(item, Item.objects.all()[0])

class NewListFormTest(unittest.TestCase):
    '''NewListForm tests'''

    @unittest.skip('realisation changed')
    @patch('lists.forms.List')
    @patch('lists.forms.Item')
    def test_save_creates_new_list_and_item_from_POST_data(
        self,
        mockItem,
        mockList
    ):
        '''test: NewListForm.save creates new List and Item objects'''
        mock_item = mockItem.return_value
        mock_list = mockList.return_value
        user = Mock()
        form = NewListForm(data={'text': 'new item text'})
        form.is_valid()

        def check_item_text_and_list():
            '''check item.text and item.list attibutes'''
            self.assertEqual(mock_item.text, 'new item text')
            self.assertEqual(mock_item.list, mock_list)
            self.assertTrue(mock_list.save.called)

        mock_item.save.side_effect = check_item_text_and_list

        form.save(owner=user)

        self.assertTrue(mock_item.save.called)

    @patch('lists.forms.List.create_new')
    def test_save_creates_new_list_from_post_data_if_user_not_authenticated(
        self,
        mock_List_create_new
    ):
        '''test: NewListForm.save users List.create_new for not authenticated users'''
        user = Mock(is_authenticated=False)
        form = NewListForm(data={'text': 'new item text unauth'})
        form.is_valid()
        form.save(owner=user)
        mock_List_create_new.assert_called_once_with(
            item_text = 'new item text unauth'
        )

    @patch('lists.forms.List.create_new')
    def test_save_creates_new_list_from_post_data_if_user_is_authenticated(
        self,
        mock_List_create_new
    ):
        '''test: NewListForm.save users List.create_new for not authenticated users'''
        user = Mock(is_authenticated=True)
        form = NewListForm(data={'text': 'new item text auth'})
        form.is_valid()
        form.save(owner=user)
        mock_List_create_new.assert_called_once_with(
            item_text = 'new item text auth',
            owner = user
        )

    @patch('lists.forms.List.create_new')
    def test_save_returns_new_list_object(
        self,
        mock_List_create_new
    ):
        '''test: form.save returns new list object'''
        user = Mock(is_authenticated=True)
        form = NewListForm(data={'text': 'new save test'})
        form.is_valid()
        ret = form.save(owner=user)
        self.assertEqual(ret, mock_List_create_new.return_value)
