from django.shortcuts import render
from .models import products
# Create your views here.

def home (request):
    
    products_to_post = products.get_all_products()
    return render(request,'home.html',{'products_to_post':products_to_post})

def detail_view(request,id):
    products_to_post = products.objects.get(id=id)
    return render(request,'view_details.html',{'products_to_post':products_to_post})
