from django.test import TestCase
from lists.forms import ItemForm
import unittest

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
