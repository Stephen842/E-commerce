from django.contrib import admin
from django.urls import path, include 
from django.conf import settings
from .import views 
from django.contrib.auth import views as auth_views

urlpatterns = [
        path('', views.Index, name='homepage'), 
        path('store', views.Store, name='store'), 
        path('signup', views.Signup, name='signup'),
        path('login', views.Signin, name='login'), 
        path('logout', views.logout, name='logout'),
        path('cart', views.Cart, name='cart'), 
        path('check-out', views.CheckOut, name='checkout'), 
        path('orders', views.Order, name='orders'),
        ]
