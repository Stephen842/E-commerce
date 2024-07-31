from django.shortcuts import render, redirect, HttpResponseRedirect 
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.template import loader
from datetime import datetime
from django.views import View 
from django.contrib.auth.hashers import check_password, make_password 
from .models import Category, Customer, Products, Order

# Create your views here.

def home(request):
    context = {
            'title': 'Rinx Venture: Your One-Stop Store for Phones, Gadgets & Repairs'
    }
    return render(request, 'pages/home.html', context)

class Index(View):
    
    def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.POST.get('cart')

        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity-1
                else:
                    cart[product] = quantity+1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        print('cart', request.session['cart'])
        return redirect('homepage')

    def get(self, request):
        return HttpResponseRedirect(f'/store{request.get_full_path()[1:]}')

def Store(request):
    cart = request.session.get('cart')

    if not cart:
        request.session['cart'] = {}

    products = None
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')

    if categoryID:
        products = Products.get_all_products_by_categoryid(categoryID)
    else:
        products = Products.get_all_products()

    data = {}
    data['products'] = products
    data['categories'] = categories

    context = {
        'title': 'Rinx Venture: Your One-Stop Store for Phones, Gadgets & Repairs',
        'data': data,
    }

    print('You are: ', request.session.get('email'))
    return render(request, 'pages/home.html', context)

#this is for the signin option, which uses field from the Customer found in the models.py
class Signin(View):
    return_url = None


    # Handles GET requests by rendering the login template for users to enter their credentials.
    # If a 'return_url' parameter is present in the request, it is saved for later redirection after successful login.
    def get(self, request):
        Signin.return_url = request.GET.get('return_url')
        return render(request, 'pages/login.html')
    
    # Handles POST requests to authenticate users.
    # Retrieves email and password from the request, validates credentials against the database,
    # and sets the user session if authentication is successful.
    # Redirects to 'return_url' if specified, otherwise redirects to the homepage.
    # If authentication fails, renders the login page with an error message.
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None

        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id

                if Signin.return_url:
                    return HttpResponseRedirect(Signin.return_url)
                else:
                    Signin.return_url = None
                    return redirect('homepage')
            else:
                error_message = 'Invalid !!'
        else:
            error_message = 'Invalid !!'

        context = {
            'title': 'Sign in to continue',
            'error': error_message,
        }

        print(email, password)
        return render(request, 'pages/signin.html', context)

# Handles user logout by clearing the session data and redirecting to the store page.
def logout(request):
    request.session.clear()
    return redirect('store')