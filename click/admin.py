from django.contrib import admin

from click.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'is_paid','amount', 'created_date']
    list_display_links = ['user']
    save_on_top = True
