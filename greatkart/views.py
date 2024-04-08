from django.shortcuts import render
from store.models import Product
from category.models import Category

def index(request):
    list_products = Product.objects.all().filter(is_available = True)
    context = { 'products' : list_products}
    return render(request, 'home.html', context)