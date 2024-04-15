from django.shortcuts import render, get_object_or_404
from store.models import Product 
from category.models import Category
from carts.models import CartItem
from django.core.paginator import Paginator,PageNotAnInteger, EmptyPage
from carts.views import _cart_id
from django.db.models import Q
# Create your views here.
def show_store(request, category_slug = None):
    categories = None
    list_products = None
    if category_slug != None :
        categories = get_object_or_404(Category, slug = category_slug)
        list_products = Product.objects.filter(category = categories,is_available = True)
    else:
        list_products = Product.objects.all().filter(is_available = True).order_by('id')

    paginator = Paginator(list_products, 6 )
    page_num  = request.GET.get('page')
    products_by_page = paginator.get_page(page_num)
    context = { 'products' : products_by_page, 'product_count' : list_products.count()}
    return render( request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    try:
        product = Product.objects.get(category__slug = category_slug, slug = product_slug )
        in_cart = CartItem.objects.filter(cart__cart_id = _cart_id(request), product = product).exists()
    except Exception as e:
        raise e
    context = {'product' : product, 'in_cart' : in_cart}
    return render(request, 'store/product_detail.html', context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET.get('keyword')
        if keyword:
            product = Product.objects.order_by('-created_at').filter(Q(description__icontains = keyword) | Q(product_name__icontains = keyword))
            product_count = product.count()
        context = {
            'products' : product,
            'product_count' : product_count
        }
    return render(request, 'store/store.html', context)