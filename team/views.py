from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse

from team.models import Team, UserTeam
from team.forms import AddCollaboratorForm


@login_required
def user_team_view(request):
    """"Return page to add a user to a team or submit form"""
    user = request.user
    users_in_team = UserTeam.objects.filter(
        ut_team=user.team_owner.pk).exclude(ut_user=user.pk)

    # Try to add a User in Team as collaborator aka team member
    # Users that belong to a team are called collaborators
    if request.method == 'POST':
        add_collaborator_form = AddCollaboratorForm(request.POST)
        if add_collaborator_form.is_valid():
            new_collaborator = User.objects.get(
                email=request.POST['email_to_add'])
            team2assign = Team.objects.get(tem_owner=user)

            # Check if user is already a team collaborator
            if users_in_team.filter(ut_user=new_collaborator):
                messages.error(
                    request,
                    f'{new_collaborator.email} '
                    'is already a Collaborator in the Team'
                )
            else:
                try:
                    # Try to create the relationship User Team
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
            # Feedback to user when form is not valid
            messages.error(
                request, 'Please ensure the email belongs to a Tasking user')
            messages.error(
                request,
                'Only registered Tasking users can collaborate in teams'
            )

    # Return form to add a User in a Team
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
