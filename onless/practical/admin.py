from django.contrib import admin

# Register your models here.
from practical.models import *


@admin.register(Practical)
class PracticalAdmin(admin.ModelAdmin):
    list_display = ['id', 'instructor', 'pupil', 'training_time']
    list_display_links = ['instructor']
    save_on_top = True


@admin.register(DayOfWeek)
class DayOfWeekAdmin(admin.ModelAdmin):
    list_display = ['id', 'instruktor', 'day']
    save_on_top = True


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['id', 'model', 'state_number']
    save_on_top = True

    """
    admin form foreign key user filter
    """

    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['instructor'].queryset = User.objects.filter(role='6')
        return super(CarAdmin, self).render_change_form(request, context, *args, **kwargs)


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'is_nationality']
    save_on_top = True
