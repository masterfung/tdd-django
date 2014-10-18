from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from .models import Item, List


def home_page(request):
    return render(request, 'home.html')


def the_best(request, list_id):
    return_list = List.objects.get(id=list_id)
    items = Item.objects.filter(list=return_list)
    return render(request, 'list.html', {'items': items})


def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/%d/' % (list_.id,))