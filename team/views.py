from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView

from tasks.models import Team, UserTeam
from team.forms import AddCollaboratorForm


# class UserTeamView(View):
#     template_name = 'team/team_collaborators.html'

#     def get(self, request, *args, **kwargs):
#         user = request.user
#         users_in_team = UserTeam.objects.filter(
#             ut_team=user.team_owner.pk).exclude(ut_user=user.pk)
#         add_collaborator_form = AddCollaboratorForm()
#         context = {
#             'users_in_team': users_in_team,
#             'add_collaborator_form': add_collaborator_form,
#         }
#         return render(
#             request, self.template_name, context=context)


def user_team_view(request):
    user = request.user
    users_in_team = UserTeam.objects.filter(
        ut_team=user.team_owner.pk).exclude(ut_user=user.pk)

    if request.method == 'POST':
        add_collaborator_form = AddCollaboratorForm(request.POST)
        if add_collaborator_form.is_valid():
            new_collaborator = User.objects.filter(
                email=request.POST['email_to_add'])
            team2assign = Team.objects.filter(tem_owner=user.team_owner.pk)
            print('\n ALREADY IN TEAM', new_collaborator, users_in_team)
            print('\n IN TEAM ? ', new_collaborator in users_in_team)
            if new_collaborator in users_in_team:
                messages.error(
                    request,
                    f'Unable to add {new_collaborator.email} in the Team'
                )
                messages.error(
                    request, 'User is already a Collaborator in the Team')
                return redirect(reverse('team_collaborators'))
            else:
                try:
                    add_user_team = UserTeam.objects.create(
                        ut_user=new_collaborator, ut_team=team2assign)
                    add_user_team.save()
                    messages.success(request, 'Added to your Team!')
                    return redirect(reverse('team_collaborators'))
                except Exception as e:
                    print('\n\nEXCEPTION', e)
                    messages.error(
                        request,
                        f'Unable to add {new_collaborator.email} in the team'
                    )
                    messages.error(request, 'Please try again')
    else:
        add_collaborator_form = AddCollaboratorForm()

    add_collaborator_form = AddCollaboratorForm()
    context = {
        'users_in_team': users_in_team,
        'add_collaborator_form': add_collaborator_form,
    }
    return render(
        request,
        'team/team_collaborators.html',
        context=context,
    )
