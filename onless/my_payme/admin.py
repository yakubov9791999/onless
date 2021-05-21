from django.contrib import admin
from my_payme.models import Transaction


class TransactionModelAdmin(admin.ModelAdmin):

    def get_status(self, obj):
        return obj.get_status_display()

    get_status.short_description = 'status'

    search_fields = ('request_id',)
    list_display = ['trans_id', 'request_id', 'amount', 'account', 'get_status', 'create_time', 'pay_time']


admin.site.register(Transaction, TransactionModelAdmin)
