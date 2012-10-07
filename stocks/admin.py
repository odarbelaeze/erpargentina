from django.contrib import admin

from stocks.models import Product
from stocks.models import PriceTag

class PriceInline(admin.TabularInline):
    """docstring for PriceInline"""
    model = PriceTag
    extra = 1
        

class ProductAdmin(admin.ModelAdmin):
    """docstring for ProductAdmin"""
    model = Product
    inlines = [PriceInline]
    list_display = ['name', 'get_price', 'stock_level', 'available']
    search_fields = ['name', 'reference']

class PriceTagAdmin(admin.ModelAdmin):
    """docstring for PriceTagAdmin"""
    model = PriceTag
    list_display = ['__unicode__', 'date', 'price']
    list_filter = ['date', 'product']
    search_fields = ['product__name', 'product__reference']

admin.site.register(Product, ProductAdmin)
admin.site.register(PriceTag, PriceTagAdmin)