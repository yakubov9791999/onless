from django.contrib import admin
from django.contrib.admin.forms import AdminPasswordChangeForm

from quiz.admin import ChoiceInline
from sign.models import *
from .models import *
from django.contrib import admin
from .models import Payment


@admin.register(EducationCategory)
class EducationCategoryAdmin(admin.ModelAdmin):
    list_display = ('title','sort')
    save_on_top = True

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'role', 'name', 'username', 'phone', 'group', 'turbo', 'birthday', 'is_active',
                    'is_superuser', 'is_staff', 'date_joined',
                    'last_login']
    list_display_links = ['role', 'name']
    list_filter = ['role', 'is_active', 'is_offline', 'school', ]
    search_fields = ['name', 'username', 'phone', 'pasport', 'turbo', ]
    save_on_top = True

    def save_model(self, request, obj, form, change):
        obj.set_password(obj.turbo)
        obj.username = obj.pasport
        obj.save()
        return super().save_model(request, obj, form, change)


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):

    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['director'].queryset = User.objects.filter(role=2)

        context['adminform'].form.fields['district'].queryset = District.objects.all()
        return super().render_change_form(request, context, *args, **kwargs)

    list_display = ['id', 'title', 'director', 'phone']
    list_display_links = ['title']
    search_fields = ['title', 'director__name', 'phone']
    list_filter = ['title', ]
    save_on_top = True


class DistrictInline(admin.StackedInline):
    model = District
    extra = 13


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title', 'state_number_code']}),
    ]
    inlines = [DistrictInline]


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'text']
    list_display_links = ['user']
    save_on_top = True


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display_links = ['category', ]
    list_display = ['id', 'category', 'number', 'year', ]
    list_filter = ['is_active', 'category', 'number', ]


@admin.register(Pay)
class PayAdmin(admin.ModelAdmin):
    list_display = ['id', 'pupil', 'payment', 'pay_date']
    list_display_links = ['pupil', ]
    list_filter = ['pupil', 'pay_date']
    save_on_top = True


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'pupil', 'teacher','is_visited', 'created_date', 'updated_date']
    list_display_links = ['subject']
    list_filter = ['created_date', 'updated_date']
    search_fields = ['subject', 'pupil', 'teacher', ]
    save_on_top = True


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'score', 'pupil', 'teacher', 'created_date']
    list_display_links = ['subject']
    list_filter = ['score', 'created_date']
    search_fields = ['subject', 'pupil', 'teacher', ]
    save_on_top = True


@admin.register(Sms)
class SmsAdmin(admin.ModelAdmin):
    list_display = ['id', 'text','sms_count', 'school']
    list_display_links = ['text', ]
    list_filter = ['school']
    save_on_top = True

@admin.register(BuySms)
class BuySmsAdmin(admin.ModelAdmin):
    list_display = ['id', 'school','sms_count', 'money']
    list_display_links = ['school', ]
    list_filter = ['school',]
    save_on_top = True

@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ['id', 'pay']
    list_display_links = ['pay', ]
    list_filter = ['pay']
    save_on_top = True


class PaymentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Payment, PaymentAdmin)