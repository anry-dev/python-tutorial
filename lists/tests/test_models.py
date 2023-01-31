from django.test import TestCase
from lists.models import Item, List
from django.core.exceptions import ValidationError
from django.urls import reverse

class ListAndItemModelTest(TestCase):
    '''List elements model tests'''

    def test_saving_and_retrieving_items(self):
        '''test to save and retrieve an item'''

        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'Just the first item!'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'The second item.'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'Just the first item!')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'The second item.')
        self.assertEqual(second_saved_item.list, list_)

    def test_cannon_save_empty_list_items(self):
        '''тест: нельзя добавлять пустые элементы в список'''

        list_ = List.objects.create()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_get_absolute_url(self):
        '''test: test getting absolute url for the model'''
        list_ = List.objects.create()
                               #/lists/{list_.id}/
        self.assertEqual(list_.get_absolute_url(),
                        reverse('view_list', args=[list_.id]))
