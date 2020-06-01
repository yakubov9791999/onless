from django.contrib import admin

# Register your models here.
from sign.models import *

admin.site.register(SignCategory)
admin.site.register(Sign)