from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView

from tasks.models import Team, UserTeam


class UserTeamView(View):
    template_name = 'accounts/profile.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        users_in_team = UserTeam.objects.filter(
            ut_team=user.team_owner.pk).exclude(ut_user=user.pk)

        return render(
            request, self.template_name, {'users_in_team': users_in_team}, )


class UserTeamCreate(CreateView):
    model = UserTeam
    fields = ['first_name', 'last_name', 'username', 'email', ]
    template_name = 'accounts/update_profile.html'
    success_url = reverse_lazy('profile')
