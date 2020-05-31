from django.contrib import admin
from django.utils.safestring import mark_safe
from user.models import User
from .models import *

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'duration']
    list_display_links = ['title', 'description']
    save_on_top = True

    # def get_likes(self, User):
    #     if obj.rating_likes.exists():
    #         return ''
    #         # return ",".join([user.username for user in obj.rating_likes.all()])
    #     else:
    #         return ''
#
# @admin.register(ResultQuiz)
# class ResultQuizAdmin(admin.ModelAdmin):
#     list_display = ['id', 'questions', 'answers']
#     list_display_links = ['id', 'questions']
#     save_on_top = True
#
# @admin.register(Question)
# class ResultQuizAdmin(admin.ModelAdmin):
#     list_display = ['id', 'title', 'video', 'get_img']
#     list_display_links = ['title']
#     save_on_top = True
#
#     def get_img(self, obj):
#         return mark_safe(f"<img src='{obj.img.url}' width='50px'>")
#
# @admin.register(Answer)
# class ResultQuizAdmin(admin.ModelAdmin):
#     list_display = ['id', 'questions', 'text']
#     list_display_links = ['question', 'text']
#     save_on_top = True

# admin.site.register(Video)
admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(ResultQuiz)