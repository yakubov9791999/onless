from django.contrib import admin
from django.contrib.admin.forms import AdminPasswordChangeForm

from quiz.admin import ChoiceInline
from .models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'role', 'name', 'username', 'phone', 'email', 'turbo', 'birthday', 'is_active',
                    'is_superuser', 'is_staff', 'date_joined',
                    'last_login']
    list_display_links = ['username', 'role']
    list_filter = ['role', 'school']
    search_fields = ['name', 'username', 'phone', 'role', 'pasport']
    save_on_top = True


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):

    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['director'].queryset = User.objects.filter(role=2)

        context['adminform'].form.fields['district'].queryset = District.objects.all()
        return super().render_change_form(request, context, *args, **kwargs)

    list_display = ['id', 'title', 'director', 'phone']
    list_display_links = ['title']
    search_fields = ['title', 'director', 'phone', 'username', 'pasport']
    list_filter = ['title', ]
    save_on_top = True


class DistrictInline(admin.StackedInline):
    model = District
    extra = 13


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title']}),
    ]
    inlines = [DistrictInline]


@admin.register(Contact)
class ConatctAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'text']
    list_display_links = ['name']
    save_on_top = True


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display_links = ['category',]
    list_display = ['id', 'category', 'number', 'year',]
    list_filter = ['is_active', 'category', 'number',]


@admin.register(Pay)
class PayAdmin(admin.ModelAdmin):
    list_display = ['id', 'pupil', 'payment', 'pay_date']
    list_display_links = ['pupil', ]
    list_filter = ['pupil', 'pay_date']
    save_on_top = True
