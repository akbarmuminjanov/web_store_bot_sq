from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register([User, History])

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ['name']


@admin.register(SubCategory)
class SubcategoryAdmin(admin.ModelAdmin):
    fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = ['name', 'price', 'available']
    search_fields = ['product_id', 'name', 'price']


