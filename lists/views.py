from django.shortcuts import redirect, render
from lists.models import Item, List
from lists.forms import ItemForm, ExistingListItemForm, NewListForm
from django.core.exceptions import ValidationError

import logging
logger = logging.getLogger(__name__)

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

def new_list2(request):
    '''new list - version 2'''

    form = NewListForm(data=request.POST)
    if form.is_valid():
        list_ = form.save(owner=request.user)
        return redirect(str(list_.get_absolute_url()))

    return render(request, 'home.html', {'form': form})

def new_list(request):
    '''new list'''

    if request.method == 'POST':
        form = ItemForm(data=request.POST)
        if form.is_valid():
            list_ = List()
            list_.owner = request.user
            list_.save()
            form.save(for_list=list_)
            return redirect(str(list_.get_absolute_url()))
        else:
            return render(request, 'home.html', {'form': form})

    return redirect('/')

def user_lists(request, email):
    '''per-user lists view'''

    owner = User.objects.get(email=email)

    return render(request, 'user_lists.html', {'owner': owner,})

