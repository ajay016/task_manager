from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import *

# Register your models here.
# User = get_user_model()

class PhotoAdmin(admin.ModelAdmin):
    list_display = ['id', 'image']

admin.site.register(User)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Task)
