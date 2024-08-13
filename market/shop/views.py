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
from .models import Category, Customer, Products, Comment, Order
from .forms import CustomerForm, SigninForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from datetime import datetime
from django.urls import reverse
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

        # I updated this below to render the same page with updated context instead of redirecting to the homepage
        return self.get(request)

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
        'cart': cart,
    }

    context = {
        'title': 'Rinx Venture: Your One-Stop Store for Phones, Gadgets & Repairs',
        'data': data,
        'date': date,
    }

    print('You are: ', request.session.get('email'))
    return render(request, 'pages/home.html', context)

@login_required
def Product_details(request, id):
    all_product = Products.objects.get(id=id)
    date = datetime.now()

     # Logic for related products: Get other products from the same category
    related_products = Products.objects.filter(category=all_product.category).exclude(id=all_product.id)

    #This below is for the comment section of each product
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            customer = Customer.objects.get(name=request.user.name)  # Get the Customer instance
            comment = Comment(
                        author = customer,  # Assign the Customer instance
                        body = form.cleaned_data['body'],
                        post = all_product,
                    )
            comment.save()
            return redirect(request.path_info)

    comments = Comment.objects.filter(post=all_product)

    context = {
        'all_product': all_product,
        'related_products': related_products,
        'comments': comments,
        'date': date,
    }
    return render(request, 'pages/product-details.html', context)

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
                try:
                    customer = Customer.objects.get(email=user.email)
                    request.session['customer'] = customer.id
                except Customer.DoesNotExist:
                    return HttpResponse('Customer does not exist for this user')
                return redirect('homepage')
            else:
                return HttpResponse('Invalid login')
        return render(request, 'pages/signin.html', {'form': form})


# Handles user logout by clearing the session data and redirecting to the store page.
def logout(request):
    request.session.clear()
    return redirect('homepage')

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
            return redirect('homepage')
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
            quantity = cart[str(product.id)]
            total_price = int(product.price.replace(',', '')) * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total_price': total_price, 
            })

        context = {
                'title': 'Your Cart',
                'cart_items': cart_items,
                'date': date,
        }

        return render(request, 'pages/cart.html', context)

@method_decorator(login_required, name='dispatch')
class CheckOut(View):
    def get(self, request):
        #If request is GET it should render the checkout form
        return render(request, 'pages/checkout.html')

    def post(self, request):
        #To process checkout form
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer_id = request.session.get('customer')
        cart = request.session.get('cart')

        if not customer_id or not cart:
            return redirect('homepage') #Redirect user to homepage if user is not logged in or there nothing is in the cart

        products = Products.get_products_by_id(list(cart.keys()))
        customer = Customer.objects.get(id=customer_id)

        for product in products:
            quantity = cart.get(str(product.id))
            total_price = int(product.price.replace(',', '')) * quantity

            order = Order(
                        customer = customer,
                        products = product,
                        price = total_price,
                        address = address,
                        phone = phone,
                        quantity = quantity
                    )
            order.save()
        request.session['cart'] = {}

        return redirect('order-confirm')


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

@login_required
def order_confirm(request):
    shop_url = reverse('store')
    context = {
        'title': 'Order Placed Successfully',
        'shop_url': shop_url
    }
    return render(request, 'pages/order_confirm.html', context)
    
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
    return render(request, 'pages/search_results.html', context)
