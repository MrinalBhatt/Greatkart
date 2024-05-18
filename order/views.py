from django.shortcuts import render,redirect
from django.urls import reverse
import paypalrestsdk
from paypalrestsdk import Payment
from django.http import HttpResponse, HttpResponseRedirect
from carts.models import Cart, CartItem
from .models import Order
from .forms import OrderForm
import datetime
import requests
import json
from django.conf import settings


# Create your views here.
def place_order(request, total = 0, quantity = 0):
    current_user    = request.user
    cart            = Cart.objects.get(user = current_user)
    cart_items      = CartItem.objects.filter(cart = cart)
    cart_count      = cart_items.count()
    tax             = 0
    grand_total     = 0
    for cart_item in cart_items:
        total       += ( cart_item.product.price * cart_item.quantity )
        quantity    += cart_item.quantity
    tax         = ( 2 * total ) /100
    grand_total = total + tax
    #check if cart item available or not
    if cart_count <= 0:
        return redirect('store')
    else:
        if request.method == 'POST':
            form = OrderForm(request.POST)
            if form.is_valid():
                data = Order()
                data.first_name     = form.cleaned_data['first_name']
                data.last_name      = form.cleaned_data['last_name'] 
                data.phone          = form.cleaned_data['phone'] 
                data.email          = form.cleaned_data['email'] 
                data.address_line1  = form.cleaned_data['address_line1'] 
                data.address_line2  = form.cleaned_data['address_line2'] 
                data.country        = form.cleaned_data['country'] 
                data.state          = form.cleaned_data['state'] 
                data.city           = form.cleaned_data['city'] 
                data.pincode        = form.cleaned_data['pincode'] 
                data.order_note     = form.cleaned_data['order_note']
                data.order_total    = grand_total
                data.tax            = tax
                data.ip             = request.META.get('REMOTE_ADDR')
                data.user           = current_user
                data.save()
                yr                  = int(datetime.date.today().strftime("%Y"))
                dt                  = int(datetime.date.today().strftime('%d'))
                mt                  = int(datetime.date.today().strftime('%m'))
                d                   = datetime.date(yr,mt,dt)
                current_date        = d.strftime("%Y%m%d")
                order_number        = current_date + str(data.id)
                data.order_number   = order_number
                data.save()
                order = Order.objects.get(user = current_user, is_ordered = False, order_number = order_number)
                context = {
                    'order' : order,
                    'cart_items' : cart_items,
                    'total' : total,
                    'tax' : tax,
                    'grand_total' : grand_total
                }
                return render(request, 'orders/payment.html', context)
        else:
            return redirect('checkout')




def makePayment(request):

# Set up PayPal SDK environment
    paypalrestsdk.configure({
        "mode": "sandbox",  # Change to "live" for production
        "client_id": settings.PAYPAL_CLIENT_ID,
        "client_secret": settings.PAYPAL_CLIENT_SECRET
    })
    
# Create a PayPal payment
    paypal_payment = Payment({
        "intent": "order",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": "http://127.0.0.1:8000/order/executePayment/",
            "cancel_url": "http://127.0.0.1:8000/order/cancel/"
        },
        "transactions": [{
            "amount": {
                "total": "10.00",
                "currency": "USD"
            },
            "description": "Example Payment"
        }]
    })

    if paypal_payment.create():
        # Redirect user to PayPal for payment approval
        for link in paypal_payment.links:
            if link.rel == 'approval_url':
                return HttpResponseRedirect(link.href)
    else:
        # Handle payment creation failure
        return render(request, 'payment_error.html', {'error': paypal_payment.error})
    

def execute_payment(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')


    # Set up PayPal SDK environment
    paypalrestsdk.configure({
        "mode": "sandbox",  # Change to "live" for production
        "client_id": settings.PAYPAL_CLIENT_ID,
        "client_secret": settings.PAYPAL_CLIENT_SECRET
    })

    payment = Payment.find(payment_id)
    if payment.execute({"payer_id": payer_id}):
        # Payment executed successfully
        return render(request, 'orders/payment-success.html')
    else:
        # Handle payment execution failure
        return render(request, 'orders/payment_error.html', {'error': payment.error})



   