from django.contrib import admin
from django.urls import path, include 
from django.conf import settings
from .views import Index, Signup, Signin, logout, CheckOut, OrderView
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
        path('', Index.as_view(), name='homepage'), 
        path('store', views.Store, name='store'), 
        path('signup', Signup.as_view(), name='signup'),
        path('signin', Signin.as_view(), name='signin'), 
        path('logout', views.logout, name='logout'),
        #path('cart', views.Cart, name='cart'), 
        path('check-out', CheckOut.as_view(), name='checkout'), 
        path('orders', OrderView.as_view(), name='orders'),
        ]
