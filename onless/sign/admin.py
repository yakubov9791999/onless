from django.contrib import admin

# Register your models here.
from django.utils.safestring import mark_safe

from sign.models import *

admin.site.register(SignCategory)



@admin.register(Sign)
class SignAdmin(admin.ModelAdmin):
    list_filter = ['category', ]
    search_fields = ['title', 'category__title', 'text']
    list_display = ['id','title', 'text', 'get_img']

    def get_img(self, obj):
        return mark_safe(f"<img src='{obj.photo.url}' width=50px>")

# @admin.register(Subject)
# class SubjectAdmin(admin.ModelAdmin):
#     list_display = ('title', 'category', 'sort')
#
#
# @admin.register(Schedule)
# class ScheduleAdmin(admin.ModelAdmin):
#     list_display = ('title', 'subject', 'author','sort', 'created_date')
#     list_filter = ['subject','created_date']
#     save_on_top = True


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['id','title', 'pub_date','author','file', 'sort', 'is_active']
    list_display_links = ['title', 'pub_date','author' ]
    list_filter = ['is_active','title', 'pub_date','author', ]