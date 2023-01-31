from django import forms

class ItemForm(forms.Form):
    '''Form for an element list'''
    
    item_text = forms.CharField()
