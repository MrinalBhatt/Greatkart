from django.shortcuts import render, get_object_or_404
from store.models import Product 
from category.models import Category

# Create your views here.
def show_store(request, category_slug = None):
    categories = None
    list_products = None
    if category_slug != None :
        categories = get_object_or_404(Category, slug = category_slug)
        list_products = Product.objects.filter(category = categories,is_available = True)
    else:
        list_products = Product.objects.all().filter(is_available = True)
    context = { 'products' : list_products, 'product_count' : list_products.count()}
    return render( request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    try:
        product = Product.objects.get(category__slug = category_slug, slug = product_slug )
    except Exception as e:
        raise e
    context = {'product' : product}
    return render(request, 'store/product_detail.html', context)