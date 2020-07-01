from django.contrib import admin

# Register your models here.
from sign.models import *

admin.site.register(SignCategory)
admin.site.register(Sign)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'sort')


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'author','sort', 'pub_date')


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['id','title', 'pub_date','author','file', 'sort', 'is_active']
    list_display_links = ['title', 'pub_date','author' ]
    list_filter = ['is_active','title', 'pub_date','author', ]