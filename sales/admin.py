from django.contrib import admin

from sales.models import *

class TiketLineInline(admin.TabularInline):
    model = TiketLine
    extra = 2

class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 2
        

class SaleAdmin(admin.ModelAdmin):
    model = Sale
    inlines = [TiketLineInline, PaymentInline]   
        

admin.site.register(Sale, SaleAdmin)
admin.site.register(Payment)