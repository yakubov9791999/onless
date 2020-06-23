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