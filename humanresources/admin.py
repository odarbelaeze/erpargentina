from django.contrib import admin

from humanresources.models import *

class PayingInline(admin.TabularInline):
	model = Paying
	extra = 0

class EarningInline(admin.TabularInline):
	model = Earning
	extra = 0
		
class WorkerAdmin(admin.ModelAdmin):
	model = Worker
	list_display = ['__unicode__', 'total_payments', 'total_earnings', 'total_payings', 'balance']
	inlines = [PayingInline, EarningInline]
		

admin.site.register(Worker, WorkerAdmin)
# admin.site.register(Paying)
# admin.site.register(Earning)