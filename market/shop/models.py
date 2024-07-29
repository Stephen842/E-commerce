from django.db import models
import datetime
from PIL import Image

# Create your models here.

#This is for the category aspect of this project with a name field to be used in
#categorizing product

class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'Categories'

    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    def __str__(self):
        return self.name


#this Customer is meant to check on users who have used the platform frequently
#Having a method to register and retrieve customer by email and to check the existence of a customer

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length = 20)
    password = models.CharField(max_length=30)

    #to save the above data
    def register(self):
        self.save()

    #To retrieve customer by their email 
    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.object.get(email=email)
        except:
            return False

    #To check if a customer exist through email
    def isExists(self):
        if Customer.objects.filter(email=self.email):
            return True
        return False

#this is for the product, which contain all neccessary details to be added to the product
#it include a static method where one can retrieve a product by it ID, category Id and to retrieve all product

class Products(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.TextField()
    image_0 = models.ImageField(upload_to='media/')
    image_1 = models.ImageField(upload_to='media/')
    image_2 = models.ImageField(upload_to='media/')
    image_3 = models.ImageField(upload_to='media/')

    class Meta:
        verbose_name_plural = 'Products'

    #To retrieve product by its ID
    @staticmethod
    def get_products_by_id(ids):
        return Products.objects.filter(id__in=ids)

    #To get retrieve product stored in the database
    @staticmethod
    def get_all_products():
        return Products.objects.all()

    #To retrieve product using category ID
    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Products.objects.filter(category=category_id)
        else:
            return Products.get_all_Products()

#This is for the order model, where users fill the neccessary products they are ordering for and then the orders are been submitted

class Order(models.Model):
    products = models.ForeignKey(Products, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField(max_length=400, blank=False)
    phone = models.CharField(max_length=30, blank=False)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def placeOrder(self):
        self.save()

    #To retrieve an order using customer ID
    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer=customer_id).order_by('-date')
