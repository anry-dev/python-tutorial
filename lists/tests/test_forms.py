from django.test import TestCase
from lists.forms import ItemForm

class ItemFormTest(TestCase):
    '''testing forms for elements lists'''

    def test_form_renders_item_text_input(self):
        '''test: form shows text input field'''
        form = ItemForm()
        self.fail(form.as_p())
