from django.contrib import admin
from django.urls import path, include 
from django.conf import settings
from .views import Index, Signup, logout, Cart, CheckOut, OrderView, Signin
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
        path('phone-repair/', views.Phone_repair, name='phone-repair'),
        path('contacts/', views.Contact, name='contacts'),
        path('', Index.as_view(), name='homepage'), 
        path('store/', views.Store, name='store'),
        path('product-details/<int:id>', views.Product_details, name='product-details'),
        path('signup/', Signup.as_view(), name='signup'),
        path('login/', views.Signin, name='login'), 
        path('logout/', views.logout, name='logout'),
        path('cart/', Cart.as_view(), name='cart'), 
        path('checkout/', CheckOut.as_view(), name='checkout'), 
        path('orders/', OrderView.as_view(), name='orders'),
        path('order-confirm/', views.order_confirm, name='order-confirm'),
        path('search/', views.search, name='search'),
        path('success/', views.Success, name='success'),
        path('404/', views.error_404, name='404')
        ]
