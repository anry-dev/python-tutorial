from django.shortcuts import redirect, render
from lists.models import Item, List
from lists.forms import ItemForm, ExistingListItemForm
from django.core.exceptions import ValidationError
from django.contrib import auth

User = auth.get_user_model()

# Create your views here.

def home_page(request):
    '''home page'''

    return render(request, 'home.html', {'form': ItemForm()})

def view_list(request, list_id):
    '''list view'''

    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)

    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)

    return render(request, 'list.html', {'list': list_, 'form': form})

def new_list(request):
    '''new list'''

    if request.method == 'POST':
        form = ItemForm(data=request.POST)
        if form.is_valid():
            list_ = List.objects.create()
            list_.owner = request.user
            form.save(for_list=list_)
            return redirect(list_)
        else:
            return render(request, 'home.html', {'form': form})

    return redirect('/')

def user_lists(request, email):
    '''per-user lists view'''

    owner = User.objects.get(email=email)

    return render(request, 'user_lists.html', {'owner': owner,})

