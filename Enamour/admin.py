from django.contrib import admin
from .models import payment_stats


class payment_statsAdmin(admin.ModelAdmin):
	list_display = ('status', 'firstname', 'amount', 'txnid', 'productinfo')


admin.site.register(payment_stats)
