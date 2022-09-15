from django.shortcuts import redirect, render
from lists.models import Item

# Create your views here.

def home_page(request):
    '''home page'''

    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/lists/the_uniq_url_in_the_world/')

    return render(request, 'home.html')

def view_list(request):
    '''list view'''

    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})
