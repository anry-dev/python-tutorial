from django.test import TestCase
from lists.forms import EMPTY_ITEM_ERROR, ItemForm
import unittest
from lists.models import Item, List

class ItemFormTest(TestCase):
    '''testing forms for elements lists'''

    @unittest.skip("not needed - just for history")
    def test_form_renders_item_text_input(self):
        '''test: form shows text input field'''
        form = ItemForm()
        self.fail(form.as_p())

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
