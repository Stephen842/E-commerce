from django.shortcuts import render, redirect, HttpResponseRedirect 
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.template import loader
from datetime import datetime
from django.views import View
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import login, authenticate
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

def Signin(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('homepage')
        form = SigninForm()
        return render(request, 'pages/signin.html', {'form': form})

    if request.method == 'POST':
        form = SigninForm(request.POST)

        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('homepage')
            else:
                return HttpResponse('Invalid login')
        return render(request, 'pages/signin.html')


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
