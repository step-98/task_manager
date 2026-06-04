from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from tasks.models import Task, Worker, TaskType, Position

admin.site.register(TaskType)
admin.site.register(Position)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "deadline",
        "is_completed",
        "priority",
        "task_type",
    )
    list_select_related = ("task_type",)
    list_filter = (
        "deadline",
        "is_completed",
        "priority",
        "task_type",
        "assignees"
    )
    search_fields = ("name", "assignees__username")


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position", )
    list_select_related = ("position", )
    fieldsets = UserAdmin.fieldsets + (
        ("Additional info", {"fields": ("position", )}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional info",
         {"fields": ("first_name", "last_name", "position", )}
         ),
    )
    search_fields = ("username", "first_name", "last_name",)
