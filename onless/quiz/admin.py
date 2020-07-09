from django.contrib import admin
from django.utils.safestring import mark_safe
from user.models import User
from .models import *
#
# @admin.register(Video)
# class VideoAdmin(admin.ModelAdmin):
#     list_display = ['id', 'title', 'description', 'duration']
#     list_display_links = ['title', 'description']
#     save_on_top = True
#
#     # def get_likes(self, User):
#     #     if obj.rating_likes.exists():
#     #         return ''
#     #         # return ",".join([user.username for user in obj.rating_likes.all()])
#     #     else:
#     #         return ''
# #
# # @admin.register(ResultQuiz)
# # class ResultQuizAdmin(admin.ModelAdmin):
# #     list_display = ['id', 'questions', 'answers']
# #     list_display_links = ['id', 'questions']
# #     save_on_top = True
# #
# # @admin.register(Question)
# # class ResultQuizAdmin(admin.ModelAdmin):
# #     list_display = ['id', 'title', 'video', 'get_img']
# #     list_display_links = ['title']
# #     save_on_top = True
# #
# #     def get_img(self, obj):
# #         return mark_safe(f"<img src='{obj.img.url}' width='50px'>")
# #
# # @admin.register(Answer)
# # class ResultQuizAdmin(admin.ModelAdmin):
# #     list_display = ['id', 'questions', 'text']
# #     list_display_links = ['question', 'text']
# #     save_on_top = True
#
# # admin.site.register(Video)

class ChoiceInline(admin.StackedInline):
    model = Answer
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['video','title', 'img','is_active']}),
    ]
    inlines = [ChoiceInline]

admin.site.register(Question, QuestionAdmin)

@admin.register(ResultQuiz)
class ResultQuizAdmin(admin.ModelAdmin):
    list_filter = ['user','answer', 'question',]



admin.site.register(Bilet)

class Choiceinline(admin.StackedInline):
    model = Javob
    extra = 3


class SavolAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['bilet','bilet_savol','video','title_uz','title_kr','title_ru', 'is_photo', 'photo','is_active']}),
    ]
    inlines = [Choiceinline]

    list_display = ['bilet','bilet_savol','title_uz','title_kr','title_ru','is_active']
    search_fields = ['bilet','title_uz','title_kr','title_ru',]
    list_filter = ['is_active','bilet', 'video',]
    save_on_top = True
    save_as_continue = True
    list_display_links = ['title_uz','title_kr','title_ru',]
admin.site.register(Savol, SavolAdmin)