from django.contrib import admin

from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'password', 'is_active', 'is_superuser', 'is_staff', 'date_joined', 'last_login']
    list_display_links = ['username', 'email']
