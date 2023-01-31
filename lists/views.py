from django.shortcuts import redirect, render
from lists.models import Item, List
from lists.forms import ItemForm
from django.core.exceptions import ValidationError

# Create your views here.

def home_page(request):
    '''home page'''

    return render(request, 'home.html', {'form': ItemForm()})

def view_list(request, list_id):
    '''list view'''

    list_ = List.objects.get(id=list_id)
    error = None

    if request.method == 'POST':
        try:
            item = Item.objects.create(text=request.POST['text'], list=list_)
            item.full_clean()
            item.save()
            return redirect(list_)
        except ValidationError:
            item.delete()
            error = "You can't have an empty list item"

    return render(request, 'list.html', {'list': list_, 'error': error})

def new_list(request):
    '''new list'''

    if request.method == 'POST':
        new_list = List.objects.create()
        item = Item.objects.create(text=request.POST['text'], list=new_list)
        try:
            item.full_clean()
            item.save()
        except ValidationError:
            new_list.delete()
            error = "You can't have an empty list item"
            return render(request, 'home.html', {'error': error})
        return redirect(new_list)

    return redirect('/')

