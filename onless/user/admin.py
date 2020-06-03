from django.contrib import admin

from .models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'role', 'username','password', 'birthday', 'email', 'is_active', 'is_superuser', 'is_staff', 'date_joined',
                    'last_login']
    list_display_links = ['username','role', 'email']
    save_on_top = True


@admin.register(DrivingSchool)
class DrivingSchoolAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'director_fio', 'phone']
    list_display_links = ['title']
    save_on_top = True


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    list_display_links = ['title']
    save_on_top = True


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    list_display_links = ['title']
    save_on_top = True


admin.site.register(Group)