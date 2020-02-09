from django.contrib import admin

from tasks.models import Category, Importance, Status, Task, Team, UserTeam


admin.site.register(Category)
admin.site.register(Importance)
admin.site.register(Team)
admin.site.register(Status)
admin.site.register(Task)


@admin.register(UserTeam)
class UserTeamAdmin(admin.ModelAdmin):
    list_display = ('ut_user', 'ut_team', )
    list_filter = ('ut_user', 'ut_team', )
