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
    form = ItemForm()

    if request.method == 'POST':
        form = ItemForm(data=request.POST)
        if form.is_valid():
            Item.objects.create(text=request.POST['text'], list=list_)
            return redirect(list_)

    return render(request, 'list.html', {'list': list_, 'form': form})

def new_list(request):
    '''new list'''

    if request.method == 'POST':
        form = ItemForm(data=request.POST)
        if form.is_valid():
            new_list = List.objects.create()
            Item.objects.create(text=request.POST['text'], list=new_list)
            return redirect(new_list)
        else:
            return render(request, 'home.html', {'form': form})

    return redirect('/')

