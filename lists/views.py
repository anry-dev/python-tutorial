from django.shortcuts import render

# Create your views here.

def home_page(request):
    '''home page'''
    return render(request, 'home.html')
