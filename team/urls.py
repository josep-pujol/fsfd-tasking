from django.contrib.auth.decorators import login_required
from django.urls import path, reverse_lazy

from team.views import user_team_view # UserTeamCreate, UserTeamView, user_team_view


urlpatterns = [
    path('collaborators/', user_team_view, name='team_collaborators'),
    path('collaborators/add/', user_team_view, name='add_collaborator'),

    # path(
    #     'collaborators/',
    #     login_required(UserTeamView.as_view()),
    #     name='team_collaborators',
    # ),
    # path(
    #     'collaborators/add',
    #     login_required(UserTeamCreate.as_view()),
    #     name='add_collaborator',
    # ),


]
