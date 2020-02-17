from django.urls import path

from team.views import user_team_view


urlpatterns = [
    path('collaborators/', user_team_view, name='team_collaborators'),
    path('collaborators/add/', user_team_view, name='add_collaborator'),
]
