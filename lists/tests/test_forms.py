from django.test import TestCase
from lists.forms import (
        EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR,
        ItemForm, ExistingListItemForm
)

import unittest
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

class FromModelTest(TestCase):
    '''testing form internals'''

    def test_form_save_handles_saving_to_a_list(self):
        '''test: form.save method saves data to a list'''
        list_ = List.objects.create()
        form = ItemForm(data={'text': 'save test'})
        new_item = form.save(for_list=list_)
        self.assertEqual(new_item, Item.objects.first())
        self.assertEqual(new_item.text, 'save test')
        self.assertEqual(new_item.list, list_)

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
