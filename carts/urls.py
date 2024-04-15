from django.urls import path
from carts import views

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add_cart/<int:product_id>', views.add_cart, name="add_cart"),
    path('delete_cart_quantity/<int:cart_item_id>', views.delete_cart_quantity, name="delete_cart_quantity"),
    path('remove_cart_item/<int:cart_item_id>', views.remove_cart_item, name="remove_cart_item")


]