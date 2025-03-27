from django.contrib import admin # type: ignore
from .models import Category, Product, Store, ExpenseCategory, Expense, Customer
from unfold.admin import ModelAdmin

@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ('name', 'sku', 'category', 'price', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'sku', 'description')
    ordering = ('-created_at',)

@admin.register(Store)
class StoreAdmin(ModelAdmin):
    list_display = ('product', 'quantity', 'reorder_level', 'last_restocked')
    list_filter = ('last_restocked',)
    search_fields = ('product__name', 'product__sku')
    ordering = ('-last_restocked',)

@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Expense)
class ExpenseAdmin(ModelAdmin):
    list_display = ('description', 'amount', 'category', 'date', 'created_at')
    list_filter = ('category', 'date', 'created_at')
    search_fields = ('description',)
    ordering = ('-date',)

@admin.register(Customer)
class CustomerAdmin(ModelAdmin):
    list_display = ('phone_number', 'name', 'last_purchase', 'created_at')
    list_filter = ('created_at', 'last_purchase')
    search_fields = ('phone_number', 'name', 'email')
    ordering = ('-created_at',)
