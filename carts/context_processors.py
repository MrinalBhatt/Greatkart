from carts.models import Cart,CartItem
from carts.views import _cart_id
from django.http import HttpResponse
def cart_count(request):
    cart_count = 0
    try:
        if request.user.is_authenticated:
            cart_id = request.user
            cart = Cart.objects.filter(user = cart_id )
            cart_items = list()
            for ct in cart:
                cart_items = CartItem.objects.filter(cart = ct, is_active = True)
                for cart_item in cart_items:
                    cart_count += cart_item.quantity
                   
        else:
            cart_id = _cart_id(request)
            cart = Cart.objects.get(cart_id = cart_id)
            cart_items = CartItem.objects.filter(cart = cart, is_active = True)
            for cart_item in cart_items:
                cart_count += cart_item.quantity
    except (Cart.DoesNotExist, CartItem.DoesNotExist): 
        cart_count = 0

    return {'cart_count' : cart_count}
