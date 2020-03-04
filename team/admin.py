from django.contrib import admin
from team.models import Team, UserTeam


admin.site.register(Team)


@admin.register(UserTeam)
class UserTeamAdmin(admin.ModelAdmin):
    list_display = ('ut_user', 'ut_team', )
    list_filter = ('ut_user', 'ut_team', )
