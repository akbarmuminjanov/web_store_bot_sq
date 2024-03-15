from django.contrib import admin
from .models import User, History, Category, SubCategory, Product
# Register your models here.

admin.site.register([User, History])

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(SubCategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'available']
    search_fields = ['product_id', 'name', 'price']
