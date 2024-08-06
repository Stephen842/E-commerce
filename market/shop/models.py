from django.db import models
import datetime
from PIL import Image
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# Create your models here.

class CustomerManager(BaseUserManager):
    def create_user(self, email, name, phone, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not name:
            raise ValueError('Users must have a name')
        if not phone:
            raise ValueError('Users must have a phone number')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            phone=phone,
        )
        user.set_password(password)  # Hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, phone, password=None):
        user = self.create_user(
            email=email,
            name=name,
            phone=phone,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Customer(AbstractBaseUser, PermissionsMixin):  # Add PermissionsMixin here
    name = models.CharField(max_length=100, blank=False)
    email = models.EmailField(unique=True, blank=False)
    phone = models.CharField(max_length=20, blank=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Add this field
    is_superuser = models.BooleanField(default=False)  # Add this field

    objects = CustomerManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone']

    def __str__(self):
        return self.email

#This is for the category aspect of this project with a name field to be used in
#categorizing product
class Category(models.Model):
    name = models.CharField(max_length=50, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'

    @staticmethod
    def get_all_categories():
        return Category.objects.all()


#this is for the product, which contain all neccessary details to be added to the product
#it include a static method where one can retrieve a product by it ID, category Id and to retrieve all product

class Products(models.Model):
    name = models.CharField(max_length=50)
    price = models.CharField(max_length=20, default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField()
    image_0 = models.ImageField(upload_to='media/')
    image_1 = models.ImageField(upload_to='media/')
    image_2 = models.ImageField(upload_to='media/')
    image_3 = models.ImageField(upload_to='media/')

    def __str__(self):
        return self.name
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
    def get_all_products_by_categoryid(category_id=None):
        if category_id:
            return Products.objects.filter(category=category_id)
        return Products.get_all_products()
    
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