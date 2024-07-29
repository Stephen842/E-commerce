from django.contrib import admin
from tinymce.widgets import TinyMCE
from django.db import models
from .models import Category, Customer, Products, Order

# Register your models here.

class ProductsAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }

admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Products, ProductsAdmin)
admin.site.register(Order)