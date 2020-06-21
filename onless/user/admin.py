from django.contrib import admin
from django.contrib.admin.forms import AdminPasswordChangeForm

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
    
    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['director'].queryset = User.objects.filter(role=2)
        return super().render_change_form(request, context, *args, **kwargs)

    list_display = ['id', 'title', 'director', 'phone']
    list_display_links = ['title']
    search_fields = ['title', 'director', 'phone', 'username', 'pasport']
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