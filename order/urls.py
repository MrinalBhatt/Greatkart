from django.urls import path
from . import views
urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    path('makePayment/', views.makePayment, name='makePayment'),
    path('executePayment/', views.execute_payment, name='execute_payment'),

]