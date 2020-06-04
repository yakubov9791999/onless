from django.contrib import admin

# Register your models here.
from django.utils.safestring import mark_safe

from video.models import *

@admin.register(MainSection)
class TrafficSectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    list_display_links = ['title']
    save_on_top = True

@admin.register(VideoSection)
class TrafficSectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'mainsection']
    list_display_links = ['title']
    save_on_top = True


@admin.register(VideoCategory)
class VideoCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'section']
    list_display_links = ['title']
    save_on_top = True

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    list_display_links = ['title']
    save_on_top = True


@admin.register(ViewComplete)
class ViewCompleteAdmin(admin.ModelAdmin):
    list_display = ['id', 'video']
    list_display_links = ['video']
    save_on_top = True
