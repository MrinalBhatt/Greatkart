from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from django.http import  HttpResponse
from store.models import Product, VariationProduct
from .models import Cart,CartItem
from django.core.exceptions import ObjectDoesNotExist

def _cart_id(request):
    cart_id = request.session.session_key
    if not cart_id:
        cart_id = request.session.create()
    return cart_id

def add_cart(request, product_id):
    product = Product.objects.get(id = product_id)
    product_variation = []
    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]
            try:
                variation = VariationProduct.object.get(product= product, category_name__iexact = key , category_value__iexact = value)
                # print(variation)
                product_variation.append(variation)
            except:
                pass
   
        try:
            cart = Cart.objects.get(cart_id = _cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id = _cart_id(request))
        cart.save()
  
        is_cart_item_exist = CartItem.objects.filter(product = product, cart = cart).exists()
        if is_cart_item_exist:
            cart_item = CartItem.objects.filter(product = product, cart = cart)
            ex_variation_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variation.all()
                ex_variation_list.append(list(existing_variation))
                id.append(item.id)
            
            if product_variation in ex_variation_list:
                index = ex_variation_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product = product, id = item_id)
                item.quantity += 1
                item.save()
            else:
                cart_item = CartItem.objects.create(
                    product = product,
                    quantity = 1,
                    cart = cart
                )
                if len(product_variation) > 0:
                    cart_item.variation.clear()
                    cart_item.variation.add(*product_variation)
                    cart_item.save()
        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart
            )
            if len(product_variation) > 0:
                cart_item.variation.clear()
                cart_item.variation.add(*product_variation)
                cart_item.save()
    return redirect('cart')

def delete_cart_quantity(request, cart_item_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    cart_item = CartItem.objects.get(id = cart_item_id, cart = cart)
    if cart_item.quantity > 1 : 
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart') 

def remove_cart_item(request, cart_item_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    cart_item = CartItem.objects.get(id = cart_item_id, cart = cart)   
    cart_item.delete()
    return redirect('cart') 


# Create your views here.
def cart(request,quantity= 0, total = 0,  cart_item = None):
    tax = 0
    grand_total = 0
    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_items = CartItem.objects.filter(cart = cart , is_active = True)
        for cart_item in cart_items:
            total       += ( cart_item.product.price * cart_item.quantity )
            quantity    += cart_item.quantity
            tax         = ( 2 * total ) /100
            grand_total = total + tax
    except ObjectDoesNotExist:
        pass

    context = {
        'total' : total,
        'quantity' : quantity,
        'cart_items' : cart_items,
        'tax' : tax,
        'grand_total' : grand_total
    } 
    # return HttpResponse()
    # exit()
    return render(request, 'store/cart.html', context)