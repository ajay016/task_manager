from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import *

# Register your models here.
# User = get_user_model()

# Admin class for Photo model
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('image',)

# Admin class for Task model
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'due_date', 'priority', 'is_complete', 'created_at', 'updated_at', 'user')
    list_filter = ('priority', 'is_complete')
    search_fields = ('title', 'description', 'user__username')
    list_editable = ('is_complete',)
    list_per_page = 20
    list_max_show_all = 100
    date_hierarchy = 'due_date'
    actions = ['mark_as_complete', 'mark_as_incomplete']

    def mark_as_complete(self, request, queryset):
        queryset.update(is_complete=True)
    mark_as_complete.short_description = "Mark selected tasks as complete"

    def mark_as_incomplete(self, request, queryset):
        queryset.update(is_complete=False)
    mark_as_incomplete.short_description = "Mark selected tasks as incomplete"

    ordering = ('priority',)  # Sort by priority by default

# Register the admin classes
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Task, TaskAdmin)