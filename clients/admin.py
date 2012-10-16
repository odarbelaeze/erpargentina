from django.contrib import admin

from clients.models import *

class ChargeInline(admin.TabularInline):
    model = Charge
    extra = 1

class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 1

class ClientAdmin(admin.ModelAdmin):
    model = Client
    inlines = [ChargeInline, PaymentInline]
    list_display = ['__unicode__', 'route', 'total_charges', 'total_payments', 'total_debt', 'has_cancelled']
    list_filter = ['route']

admin.site.register(Route)
admin.site.register(Client, ClientAdmin)
admin.site.register(Charge)