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
from django.utils.decorators import method_decorator
from django.db.models import Q
from datetime import datetime
# Create your views here.

def home(request):
    date = datetime.now()
    context = {
            'title': 'Rinx Venture: Your One-Stop Store for Phones, Gadgets & Repairs',
            'date': date,
    }
    return render(request, 'pages/home2.html', context)

class Index(View):
    
    def post(self, request):
        product_id = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart', {})

        if product_id:
            quantity = cart.get(product_id, 0)
            if remove:
                if quantity <= 1:
                    cart.pop(product_id, None)
                else:
                    cart[product_id] = quantity - 1
            else:
                cart[product_id] = quantity + 1

        request.session['cart'] = cart
        print('cart', request.session['cart'])
        return redirect('homepage')

    def get(self, request):
        return HttpResponseRedirect(f'/store{request.get_full_path()[1:]}')

def Store(request):
    date = datetime.now()
    cart = request.session.get('cart')

    if not cart:
        request.session['cart'] = {}

    products = None
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')

    if categoryID:
        #This is to ensure that categoryID is a valid integer
        try:
            categoryId = int(categoryID)
            products = Products.get_all_products_by_categoryid(categoryID)
        except ValueError:
            products = Products.get_all_products() #If the CategoryId is invalid, it should display all products
    else:
        products = Products.get_all_products()

    data = {
        'products': products,
        'categories': categories,
    }

    context = {
        'title': 'Rinx Venture: Your One-Stop Store for Phones, Gadgets & Repairs',
        'data': data,
        'date': date,
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

@method_decorator(login_required, name='dispatch')
class Cart(View):
    def get(self, request):
        date = datetime.now()
        cart = request.session.get('cart', {})
        product_ids = list(cart.keys())
        products = Products.objects.filter(id__in=product_ids)

        cart_items = []
        for product in products:
            cart_items.append({
                'product': product,
                'quantity': cart[str(product.id)]
            })

        context = {
                'title': 'Your Cart',
                'cart_items': cart_items,
                'date': date,
        }

        return render(request, 'pages/cart.html', context)

@method_decorator(login_required, name='dispatch')
class CheckOut(View):
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer_id = request.session.get('customer')
        cart = request.session.get('cart')
        products = Products.get_products_by_id(list(cart.keys()))
        print(address, phone, customer, cart, products)

        customer = Customer.objects.get(id=customer_id)

        for product in products:
            print(cart.get(str(product.id)))
            order = Order(
                        customer = customer,
                        product = product,
                        price = product.price,
                        address = address,
                        phone = phone,
                        quantity = cart.get(str(product.id))
                    )
            order.save()
        request.session['cart'] = {}

        return redirect('cart')


@method_decorator(login_required, name='dispatch')
class OrderView(View):
    def get(self, request):
        date = datetime.now()
        customer_id = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer_id)
        print(orders)
        context = {
                'orders': orders,
                'title': '',
                'date': date,
        }
        return render(request, 'pages/orders.html', context)
    
def search(request):
    date = datetime.now()
    query = request.GET.get('q')
    products = Products.objects.filter(Q(name__icontains=query) | Q(category__name__icontains=query))
    categories = Category.objects.filter(name__icontains=query)
    
    context = {
        'query': query,
        'products': products,
        'categories': categories,
        'date': date,
    }
    return render(request, 'search_results.html', context)
