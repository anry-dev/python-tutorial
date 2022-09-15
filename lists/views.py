from django.shortcuts import redirect, render
from lists.models import Item, List

# Create your views here.

def home_page(request):
    '''home page'''

    return render(request, 'home.html')

def view_list(request, list_id):
    '''list view'''

    current_list = List.objects.get(id=list_id)
    return render(request, 'list.html', {'list': current_list})
    #items = Item.objects.filter(list=current_list)
    #return render(request, 'list.html', {'items': items})

def new_list(request):
    '''new list'''

    if request.method == 'POST':
        new_list = List.objects.create()
        Item.objects.create(text=request.POST['item_text'], list=new_list)
        return redirect(f'/lists/{new_list.id}/')

    return redirect('/')

def add_item(request, list_id):
    '''add item to the list'''

    if request.method == 'POST':
        current_list = List.objects.get(id=list_id)
        Item.objects.create(text=request.POST['item_text'], list=current_list)
        return redirect(f'/lists/{current_list.id}/')

    return redirect('/')
