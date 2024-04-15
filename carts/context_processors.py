from carts.models import Cart,CartItem
from carts.views import _cart_id

def cart_count(request):
    cart_count = 0
    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_items = CartItem.objects.filter(cart = cart, is_active = True)
        for cart_item in cart_items:
            cart_count += cart_item.quantity
    except CartItem.DoesNotExist:
        cart_count = 0
    return {'cart_count' : cart_count}
