from django.contrib import admin

from tasks.models import Category, Importance, Status, Task


admin.site.register(Category)
admin.site.register(Importance)
admin.site.register(Status)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('tsk_name', 'tsk_user', 'tsk_team', 'tsk_due_date',
                    'startdate', 'finishdate', )
    list_filter = ('tsk_user', 'tsk_team', )
