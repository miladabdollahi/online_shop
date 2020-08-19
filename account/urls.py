from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('login-register', views.login_register, name='login-register'),
    path('register/confirm', views.register_confirm, name='register-confirm'),
    path('login/confirm', views.login_confirm, name='login-confirm'),
    path('login/confirm/send-otp-code', views.send_otp_code, name='send-otp-code'),
    path('login/confirm/verified-otp-code', views.login_by_otp_confirm, name='login-by-otp-confirm'),
    path('password/reset', views.rest_password, name='passord-reset'),
]
