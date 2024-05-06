from django.shortcuts import render, redirect
import requests.utils
from .forms import SignupForm, LoginForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Accounts
from django.contrib import messages
# Create your views here.
from carts.models import Cart, CartItem
from carts.views import _cart_id

# Verification Email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

import requests
def signup(request):
    
    if request.method == "POST":
        form  = SignupForm(request.POST)
        if form.is_valid():
            first_name      = form.cleaned_data['first_name']
            last_name       = form.cleaned_data['last_name']
            email           = form.cleaned_data['email']
            password        = form.cleaned_data['password']
            phone_number    = form.cleaned_data['phone_number']
            gender          = form.cleaned_data['gender']
            user_name       = email.split('@')[0] 
            user = Accounts.objects.create_user(
                first_name = first_name,
                last_name = last_name,
                username = user_name,
                email = email,
                password = password)
            user.phone_number = phone_number
            user.gender = gender
            user.save()

            # Verification Email functionality
            current_site    = get_current_site(request)
            mail_subject    = 'Verify Your Greatkart Account'
            message         = render_to_string('accounts/account_verification_email.html', {
                'user' : user,
                'domain' : current_site,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user)
            }) 
            send_email = EmailMessage(mail_subject, message, to=[email,])
            send_email.content_subtype = 'html'
            send_email.send()

            return redirect('/accounts/login?command=verification&email='+email)
    else:
        form = SignupForm()
    context = {
        'form' : form
    }
    return render(request, 'accounts/signup.html', context)

def login_view(request):
   
    if request.method == 'POST':
        email       = request.POST.get('email')
        password    = request.POST.get('password')
        user        = authenticate(request, email = email, password = password )
        if user:
           
            cart_id                     =  _cart_id(request)
            user_cart                   = Cart.objects.filter(user = user).exists()
            if user_cart:
                is_new_user_cart        = Cart.objects.filter(cart_id = cart_id).exists()
                if is_new_user_cart:
                    new_user_cart       = Cart.objects.get(cart_id = cart_id)
                    existing_user_cart  = Cart.objects.get(user = user)
                    cart_items          = CartItem.objects.filter(cart = existing_user_cart)
                    new_cart_items      = CartItem.objects.filter(cart = new_user_cart)
                    for ext_item in cart_items:
                        for new_item in new_cart_items:
                            current_variation   = list(ext_item.variation.all())
                            new_variation       = list(new_item.variation.all())
                            if current_variation == new_variation:
                                ext_item.quantity += new_item.quantity
                                ext_item.save()
                                new_item.delete()
                    new_user_cart.user  = user
                    new_user_cart.save()
                    cart_items.update( cart = new_user_cart )
                    existing_user_cart.delete()
            else:
                try:
                    is_cart         = Cart.objects.filter(cart_id = cart_id).exists()
                    if is_cart:
                        cart        = Cart.objects.get(cart_id = cart_id)
                        cart.user   = user
                        cart.save()
                except :
                    messages.error(request,'not getting cart 2')
                    pass
            login(request, user)
            url = request.META.get('HTTP_REFERER')
            try:
                query   = requests.utils.urlparse(url).query
                params  = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                return redirect('dashboard')
        else:

            messages.error(request, "Invalid credentials!")
            return redirect('login')
    else:
        form = LoginForm()
        context = { "form" : form }
        return render(request, 'accounts/login.html', context)
    
@login_required(login_url= 'login')
def logout_view(request):
    logout(request)
    return redirect('home')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Accounts._default_manager.get(pk = uid)
    except (TypeError, ValueError, OverflowError, Accounts.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your Account is activated!')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link!')
        return redirect('signup')
    return

@login_required(login_url= 'login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')

def forgotPassword(request):
    if request.method == 'POST':
        email   = request.POST['email']
        if Accounts.objects.filter(email=email).exists():
            user = Accounts.objects.get(email__iexact = email) 
            # Verification Email functionality
            current_site    = get_current_site(request)
            mail_subject    = 'Reset Password Account'
            message         = render_to_string('accounts/forgot_password_email.html', {
                        'user' : user,
                        'domain' : current_site,
                        'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                        'token' : default_token_generator.make_token(user)
                    }) 
            send_email = EmailMessage(mail_subject, message, to=[email,])
            send_email.content_subtype = 'html'
            send_email.send()
            messages.success(request, 'We have sent you an email please check your mail box!')
            return redirect('forgotPassword')
        else:
            messages.error(request, "Invalid user!" )
            return redirect('login')
    else:
        return render(request, 'accounts/forgotPassword.html')

def resetPasswordValidation(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Accounts._default_manager.get(pk = uid)
    except (TypeError, ValueError, OverflowError, Accounts.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please set your password!')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link is expired!')
        return redirect('login')
    
def resetPassword(request):
    if request.method == 'POST':
        password            = request.POST['password']
        confirm_password    = request.POST['confirm_password']
        if password == confirm_password:
            uid         = request.session['uid']
            user        = Accounts.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password successfully changed!')
            return redirect('login')
        else:
            messages.error(request, "Password and Confirm password doen't match")
            return redirect('resetPassword')
    else:
        return render(request, 'accounts/resetPassword.html')