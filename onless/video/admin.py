from django.contrib import admin

# Register your models here.
from django.contrib.admin import SimpleListFilter
from django.utils.safestring import mark_safe

from video.models import *


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    list_display_links = ['title']
    save_on_top = True








@admin.register(ViewComplete)
class ViewCompleteAdmin(admin.ModelAdmin):
    list_display = ['id', 'video', 'user', 'get_school_name','time']
    list_display_links = ['video']
    save_on_top = True
    list_filter = ['video',]
    search_fields = ['user__phone','user__name','user__username', 'video', ]

    def get_school_name(self, obj):
        return obj.user.school



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    list_display_links = ['title']
    save_on_top = True


@admin.register(SignUpSchool)
class SignUpSchoolAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'select', 'is_active', 'phone', 'viloyat','region' ,'district','tuman', 'text', 'pub_date']
    list_display_links = ['name']
    list_filter = ['is_active','select','viloyat','region', 'district', 'tuman', 'phone', 'text', ]
    save_on_top = True
    search_fields = ['name','text','viloyat__title','region', 'district', 'tuman__title', 'phone',  ]