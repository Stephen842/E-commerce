from django.shortcuts import render, redirect, HttpResponseRedirect 
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.template import loader
from datetime import datetime
from django.views import View 
from django.contrib.auth.hashers import check_password, make_password 
from .models import Category, Customer, Products, Order
from .forms import CustomerForm, SigninForm
from django.contrib.auth.decorators import login_required
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
    #If users session is still on, user is redirected to the store page
    # If a 'return_url' parameter is present in the request, it is saved for later redirection after successful login.
    def get(self, request):
        if request.session.get('customer'):
            return redirect('store')
        Signin.return_url = request.GET.get('return_url')
        form = SigninForm()
        return render(request, 'pages/signin.html', {'form': form})
    
    # Handles POST requests to authenticate users.
    # Retrieves email and password from the request, validates credentials against the database,
    # and sets the user session if authentication is successful.
    # Redirects to 'return_url' if specified, otherwise redirects to the homepage.
    # If authentication fails, renders the login page with an error message.
    def post(self, request):
        form = SigninForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            customer = Customer.get_customer_by_email(email)

            if customer and check_password(password, customer.password):
                request.session['customer'] = customer.id
                if Signin.return_url:
                    return HttpResponseRedirect(Signin.return_url)
                else:
                    return redirect('store')
            else:
                error_message = 'Invalid email or password'
                return render(request, 'pages/signin.html', {'form': form, 'error': error_message})

        return render(request, 'pages/signin.html', {'form': form})

# Handles user logout by clearing the session data and redirecting to the store page.
def logout(request):
    request.session.clear()
    return redirect('store')

class Signup(View):
    def get(self, request):
        form = CustomerForm()
        return render(request, 'pages/signup.html', {'form': form})

    def post(self, request):
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.password = make_password(customer.password)
            customer.save()
            return redirect('store')
        else:
            return render(request, 'pages/signup.html', {'form': form})
   
class CheckOut(View):
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Products.get_products_by_id(list(cart.key()))
        print(address, phone, customer, cart, products)

        for product in products:
            print(cart.get(str(product.id)))
            order = Order(
                        customer=Customer(id=customer),
                        product = product,
                        price = product.price,
                        address = address,
                        phone = phone,
                        quantity = cart.get(str(product.id))
                    )
            order.save()
        request.session['cart'] = {}

        return redirect('cart')

class OrderView(View):
    def get(self, request):
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)
        print(orders)
        context = {
                'orders': orders,
                'title': ''
        }
        return render(request, 'pages/orders.html', context)
