from django.contrib import admin

# Register your models here.
from .models import Logs


@admin.register(Logs)
class LogsAdministrator(admin.ModelAdmin):
    list_display = ["times", 'name', 'levelname', "short_message"]

    search_fields = ["msg"]

    fieldsets = [
        (
            "Detail", {
                "fields": [
                    "name",
                    "levelname",
                    "msg",
                    "args"
                ]
            }), (
            "File Infor", {
                "fields": [
                    "pathname",
                    "funcname",
                    "lineno",
                    "threadName",
                    "processName",
                ]
            }
        ), (
            "Exc Infor", {
                "fields": [
                    "exc_info",
                    "exc_text",
                    "stack_info"
                ],
                "classes": ("collapse",),
            }
        ), (
            "Not Userful", {
                "fields": [
                    "times",
                    "msecs",
                    "relativeCreated",
                    "thread",
                    "process",
                    "levelno",
                ],
                "classes": ("collapse",),
            })
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
    
    def delete_model(self, request, obj):
        obj.delete()
        # super(LogsAdministrator, self).delete_model(request,obj)