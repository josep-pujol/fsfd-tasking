from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse

from tasks.models import Team, UserTeam
from team.forms import AddCollaboratorForm


@login_required
def user_team_view(request):
    user = request.user
    users_in_team = UserTeam.objects.filter(
        ut_team=user.team_owner.pk).exclude(ut_user=user.pk)

    if request.method == 'POST':
        add_collaborator_form = AddCollaboratorForm(request.POST)
        if add_collaborator_form.is_valid():
            new_collaborator = User.objects.get(
                email=request.POST['email_to_add'])
            team2assign = Team.objects.get(tem_owner=user)
            if users_in_team.filter(ut_user=new_collaborator):
                messages.error(
                    request,
                    f'{new_collaborator.email} '
                    'is already a Collaborator in the Team'
                )
            else:
                try:
                    add_user_team = UserTeam.objects.create(
                        ut_user=new_collaborator, ut_team=team2assign)
                    add_user_team.save()
                    messages.success(request, 'Added to your Team!')
                    return redirect(reverse('team_collaborators'))
                except Exception:
                    messages.error(
                        request,
                        f'Unable to add {new_collaborator.email} in the team'
                    )
                    messages.error(request, 'Please try again')
        else:
            messages.error(
                request, 'Please ensure the email belongs to a Tasking user')
            messages.error(
                request,
                'Only registered Tasking users can collaborate in teams'
            )

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
