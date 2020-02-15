from django.contrib.auth.decorators import login_required
from django.urls import path, reverse_lazy

from team.views import UserTeamView


urlpatterns = [
    path(
        'team/',
        login_required(UserTeamView.as_view()),
        name='team',
    ),
]
