from django.contrib import admin # type: ignore
from .models import Category, Product, Store, ProductStock, ExpenseCategory, Expense, Customer, Sale, SaleItem, ProductVariant
from unfold.admin import ModelAdmin

@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    
class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    fields = ('size', 'color', 'stock', 'price_adjustment', 'is_active')

@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ('name', 'price', 'category', 'has_variants', 'get_total_stock', 'created_at')
    list_filter = ('category', 'has_variants', 'created_at')
    search_fields = ('name', 'category__name')
    date_hierarchy = 'created_at'
    inlines = [ProductVariantInline]
    raw_id_fields = ('category',)

    def get_total_stock(self, obj):
        return obj.get_total_stock()
    get_total_stock.short_description = 'Total Stock'

@admin.register(Store)
class StoreAdmin(ModelAdmin):
    list_display = ('name', 'location', 'phone', 'email', 'updated_at')
    search_fields = ('name', 'location', 'phone', 'email')

@admin.register(ProductStock)
class ProductStockAdmin(ModelAdmin):
    list_display = ('product', 'store', 'quantity', 'reorder_level', 'last_restocked')
    list_filter = ('store', 'product')
    search_fields = ('product__name', 'store__name')
    date_hierarchy = 'last_restocked'

@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Expense)
class ExpenseAdmin(ModelAdmin):
    list_display = ('description', 'amount', 'category', 'date', 'created_at')
    list_filter = ('category', 'date')
    search_fields = ('description',)
    date_hierarchy = 'date'

@admin.register(Customer)
class CustomerAdmin(ModelAdmin):
    list_display = ('name', 'phone_number', 'email', 'last_purchase')
    search_fields = ('name', 'phone_number', 'email')
    date_hierarchy = 'last_purchase'

class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1
    fields = ('product', 'quantity', 'unit_price', 'discount', 'subtotal')
    readonly_fields = ('subtotal',)

@admin.register(Sale)
class SaleAdmin(ModelAdmin):
    list_display = ('id', 'customer', 'store', 'date', 'total_amount', 'payment_status', 'payment_method')
    list_filter = ('payment_status', 'payment_method', 'date')
    search_fields = ('customer__name', 'customer__phone_number', 'id')
    date_hierarchy = 'date'
    inlines = [SaleItemInline]
    readonly_fields = ('total_amount',)

@admin.register(SaleItem)
class SaleItemAdmin(ModelAdmin):
    list_display = ('sale', 'product', 'quantity', 'unit_price', 'discount', 'subtotal')
    list_filter = ('product',)
    search_fields = ('product__name', 'sale__id')

@admin.register(ProductVariant)
class ProductVariantAdmin(ModelAdmin):
    list_display = ('product', 'size', 'color', 'stock', 'get_final_price', 'is_active')
    list_filter = ('product', 'size', 'color', 'is_active')
    search_fields = ('product__name',)
    date_hierarchy = 'created_at'
