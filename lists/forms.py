from django import forms
from lists.models import Item, List
from django.core.exceptions import ValidationError

EMPTY_ITEM_ERROR = "You can't have an empty list item"
DUPLICATE_ITEM_ERROR = "You've already got this item in your list"

class ItemForm(forms.models.ModelForm):
    '''Form for an element list'''

    class Meta:
        model = Item
        fields = ('text',)
        widgets = {
                'text': forms.fields.TextInput(
                            attrs = {'placeholder': 'Enter a to-do item',
                                     'class': 'form-control input-lg',
                            }),
        }

        error_messages = {
                'text': {'required': EMPTY_ITEM_ERROR },
        }

    def save(self, for_list):
        self.instance.list = for_list
        return super().save()

class ExistingListItemForm(ItemForm):
    '''Form for existing list an element item'''

    def __init__(self, for_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.list = for_list

    def validate_unique(self):
        '''for unique check'''
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'text': [DUPLICATE_ITEM_ERROR]}
            self._update_errors(e)

    def save(self):
        return forms.models.ModelForm.save(self)

class NewListForm(ItemForm):
    '''Form for the new list - v2'''

    def save_pre_1(self, owner):
        '''save form data to objects'''
        list_ = List()
        if owner:
            list_.owner = owner
        list_.save()
        item = Item()
        item.list = list_
        item.text = self.cleaned_data['text']
        item.save()

    def save(self, owner):
        '''save form data to objects'''
        if owner.is_authenticated:
            return List.create_new(
                    item_text=self.cleaned_data['text'], owner=owner)
        else:
            return List.create_new(
                    item_text=self.cleaned_data['text'])
