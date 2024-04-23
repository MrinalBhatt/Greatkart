from django.urls import path
from . import views
urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('ativate/<slug:uidb64>/<slug:token>/', views.activate , name='activate'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('forgotPassword', views.forgotPassword, name='forgotPassword'),
    path('resetPasswordValidation/<slug:uidb64>/<slug:token>/', views.resetPasswordValidation, name='resetPasswordValidation'),
    path('resetPassword', views.resetPassword, name='resetPassword'),

]