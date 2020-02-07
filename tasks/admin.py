from django.contrib import admin

from tasks.models import Category, Importance, Status, Task, Team, UserTeam

admin.site.register(Category)
admin.site.register(Importance)
admin.site.register(Team)
admin.site.register(Status)
admin.site.register(Task)
admin.site.register(UserTeam)
