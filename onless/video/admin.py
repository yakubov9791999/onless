from django.contrib import admin

# Register your models here.
from django.utils.safestring import mark_safe

from video.models import *


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    list_display_links = ['title']
    save_on_top = True


@admin.register(ViewComplete)
class ViewCompleteAdmin(admin.ModelAdmin):
    list_display = ['id', 'video', 'time']
    list_display_links = ['video']
    save_on_top = True


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    list_display_links = ['title']
    save_on_top = True


@admin.register(SignUpSchool)
class SignUpSchoolAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'select', 'phone', 'region', 'district', 'text']
    list_display_links = ['name']
    save_on_top = True