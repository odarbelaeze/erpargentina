from django.contrib import admin

from stocks.models import WareHouse
from stocks.models import Product
from stocks.models import PriceTag
from stocks.models import Stock
from stocks.models import StockEvent

class PriceInline(admin.TabularInline):
    """docstring for PriceInline"""
    model = PriceTag
    extra = 1

class StockEventInline(admin.TabularInline):
    """docstring for StockInline"""
    model = StockEvent
    extra = 0

class StockInline(admin.TabularInline):
    """docstring for StockInline"""
    model = Stock
    extra = 2

class WareHouseAdmin(admin.ModelAdmin):
    """docstring for WareHouseAdmin"""
    model = WareHouse
    inlines = [StockInline, ]
    list_display = ['name', 'address']
    search_fields = ['name', 'address']

class ProductAdmin(admin.ModelAdmin):
    """docstring for ProductAdmin"""
    model = Product
    inlines = [PriceInline, StockInline, ]
    list_display = ['name', 'price', 'available', 'stock_level']
    search_fields = ['name', 'id', 'stock__warehouse__name']

class PriceTagAdmin(admin.ModelAdmin):
    """docstring for PriceTagAdmin"""
    model = PriceTag
    list_display = ['__unicode__', 'date', 'price']
    list_filter = ['date', 'product']
    search_fields = ['product__name', 'product__id']

class StockAdmin(admin.ModelAdmin):
    """docstring for StockAdmin"""
    model = Stock
    inlines = [StockEventInline, ]
    list_display = ['__unicode__', 'warehouse', 'product', 'level']
    list_editable = ['level']
    list_filter = ['warehouse', 'product']

class StockEventAdmin(admin.ModelAdmin):
    """docstring for StockEventAdmin"""
    model = StockEvent
    list_display = ['__unicode__', 'reason', 'date', 'level']
    list_filter = ['stock__product__name', 'stock', 'stock__warehouse__name']


        

admin.site.register(WareHouse, WareHouseAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(PriceTag, PriceTagAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(StockEvent, StockEventAdmin)
