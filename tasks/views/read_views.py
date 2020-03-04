from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse

from tasks.models import Status, Task


@login_required
def user_tasks(request):
    """Return page with the User personal Tasks"""
    tasks = Task.objects.filter(
        tsk_user_id=request.user.pk,
        tsk_team_id=1,
        finishdate__isnull=True
    )
    status = Status.objects.all()
    context = {
        'section_title': 'Personal Tasks',
        'is_task_editor': True,
        'tasks': tasks,
        'status': status,
    }
    return render(request, 'tasks/tasks_table.html', context=context)


@login_required
def assigned_tasks(request):
    """Return page with Tasks assigned to the User by a Team Owner"""
    user = request.user
    is_team_owner = hasattr(user, 'team_owner')
    if is_team_owner:
        ids_to_exclude = [1, user.team_owner.pk, ]
    else:
        ids_to_exclude = [1, ]
    tasks = Task.objects.filter(
        tsk_user_id=request.user.pk,
        finishdate__isnull=True
        ).exclude(tsk_team_id__in=ids_to_exclude)
    status = Status.objects.all()
    context = {
        'section_title': 'Assigned Tasks',
        'is_task_editor': False,
        'tasks': tasks,
        'status': status,
    }
    return render(request, 'tasks/tasks_table.html', context=context)


@login_required
def team_tasks(request):
    """
    Return page with the Tasks that a Team Owner has assigned to
    other users. Only visible to Team Owners
    """
    user = request.user
    is_team_owner = hasattr(user, 'team_owner')
    if is_team_owner:
        team_id = request.user.team_owner.pk
        tasks = Task.objects.filter(
            tsk_team_id=team_id, finishdate__isnull=True)
        status = Status.objects.all()
        context = {
            'section_title': "Team's Task List",
            'is_task_editor': True,
            'tasks': tasks,
            'status': status,
        }
        return render(
            request, 'tasks/tasks_table.html', context=context)
    else:
        messages.info(request, 'Only Team Owners can access a Team Task List.')
        return redirect(reverse('index'))


@login_required
def completed_tasks(request):
    """Return page with all Tasks completed by the User"""
    tasks = Task.objects.filter(
        tsk_user_id=request.user.pk, finishdate__isnull=False)
    context = {
        'section_title': 'Completed Tasks',
        'tasks': tasks,
    }
    return render(request, 'tasks/completed_tasks_table.html', context=context)
