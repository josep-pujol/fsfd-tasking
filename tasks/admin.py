from django.contrib import admin

from tasks.models import Category, Group, Importance, Status, Task, UserGroup

admin.site.register(Category)
admin.site.register(Importance)
admin.site.register(Group)
admin.site.register(Status)
admin.site.register(Task)
admin.site.register(UserGroup)
