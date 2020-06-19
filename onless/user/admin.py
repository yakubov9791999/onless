from django.contrib import admin

from .models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'role', 'name','username', 'phone','email', 'turbo', 'birthday', 'is_active', 'is_superuser', 'is_staff', 'date_joined',
                    'last_login']
    list_display_links = ['username','role']
    list_filter = ['role','school']
    search_fields = ['name', 'username', 'phone', 'role','pasport']
    save_on_top = True


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    # def queryset(self, request):
    #     qs = super(SchoolAdmin, self).queryset(request)
    #     return qs.filter(author=request.user)

    list_display = ['id', 'title', 'director', 'phone']
    list_display_links = ['title']
    search_fields = ['title', 'director', 'phone']
    list_filter = ['title', ]
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

@admin.register(Contact)
class ConatctAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'text']
    list_display_links = ['name']
    save_on_top = True

admin.site.register(Group)


@admin.register(Pay)
class PayAdmin(admin.ModelAdmin):
    list_display = ['id', 'pupil','payment', 'pay_date']
    list_display_links = ['pupil',]
    list_filter = ['pupil', 'pay_date']
    save_on_top = True