from django.test import TestCase
from lists.models import Item, List
from django.core.exceptions import ValidationError
from django.urls import reverse

class ItemModelTest(TestCase):
    '''Item elements model tests'''

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

    def test_duplicate_items_are_invalid(self):
        '''test: we can't add duplicate items into the same list'''
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='dup_test')
        with self.assertRaises(ValidationError):
            item = Item(list=list_, text='dup_test')
            item.full_clean()

    def test_CAN_save_same_item_to_different_lists(self):
        '''test: we CAN add the same items to different lists'''
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(list=list1, text='dup_test')
        item = Item(list=list2, text='dup_test')
        item.full_clean()

    def test_list_ordering(self):
        '''test: the list is ordered'''
        list_ = List.objects.create()
        item1 = Item.objects.create(list=list_, text='i1')
        item2 = Item.objects.create(list=list_, text='item 2')
        item3 = Item.objects.create(list=list_, text='3')
        self.assertEqual(
            list(Item.objects.all()),
            [item1, item2, item3]
        )

    def test_item_representation(self):
        '''test: item string representation'''
        item = Item(text='some string')
        self.assertEqual(str(item), 'some string')

    def test_default_text(self):
        '''test: default item text'''
        item = Item()
        self.assertEqual(item.text, '')

    def test_item_is_related_to_list(self):
        '''test: item element is connected to a list element'''
        list_ = List.objects.create()
        item = Item()
        item.list = list_
        item.save()
        self.assertIn(item, list_.item_set.all())

class ListModelTest(TestCase):
    '''Item elements model tests'''

    def test_get_absolute_url(self):
        '''test: test getting absolute url for the model'''
        list_ = List.objects.create()
                               #/lists/{list_.id}/
        self.assertEqual(list_.get_absolute_url(),
                        reverse('view_list', args=[list_.id]))

