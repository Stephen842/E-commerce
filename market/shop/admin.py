from django.contrib import admin
from tinymce.widgets import TinyMCE
from django.db import models
from django.db.models import Q
from .models import Category, Customer, Products, Order

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

    pass


class ProductsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category')
    search_fields = ('name', 'price')

    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        try:
            search_term_as_int = int(search_term)
            queryset |= self.model.objects.filter(Q(category__name__icontains=search_term))
        except ValueError:
            queryset |= self.model.objects.filter(Q(category__name__icontains=search_term))
        return queryset, use_distinct

class CustomerAdmin(admin.ModelAdmin):
    # Specify the fields to be displayed in the list view
    list_display = ('id','email', 'name', 'phone', 'is_active', 'is_staff')
    
    # Add filters in the right sidebar
    list_filter = ('is_active', 'is_staff')
    
    # Add a search bar at the top of the list view
    search_fields = ('email', 'name', 'phone')
    
    # Add fields to be displayed in the detail view
    fieldsets = (
        (None, {'fields': ('email', 'name', 'phone', 'is_active', 'is_staff')}),
        ('Permissions', {'fields': ('is_superuser',)}),
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Customer, CustomerAdmin)  # Register Customer with the custom admin
admin.site.register(Products, ProductsAdmin)
admin.site.register(Order)