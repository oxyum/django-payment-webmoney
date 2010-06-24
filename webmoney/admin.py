from django.contrib import admin
from webmoney.models import Invoice, Payment, Purse

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'payment_no', 'created_on', 'user', '_is_payed_admin']
    list_filter = ['created_on', 'user']
    date_hierarchy = 'created_on'
    ordering = ['-created_on', 'user']
    search_fields = ['payment_no', 'created_on']

admin.site.register(Invoice, InvoiceAdmin)

class PaymentAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_on'
    list_display = ['id', 'sys_invs_no', 'sys_trans_no', 'amount', 'invoice']
    list_filter = ['created_on']
    ordering = ['-created_on']
    search_fields = ['id']

admin.site.register(Payment, PaymentAdmin)

class PurseAdmin(admin.ModelAdmin):
    list_display = ['__unicode__']
    ordering = ['purse']
    search_fields = ['purse']

admin.site.register(Purse, PurseAdmin)
