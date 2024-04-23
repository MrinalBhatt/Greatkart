from django.shortcuts import render, redirect
from .forms import SignupForm, LoginForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Accounts
from django.contrib import messages
# Create your views here.

# Verification Email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

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
            login(request, user)
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