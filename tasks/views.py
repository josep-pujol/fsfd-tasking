from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy

from subscriptions.models import PremiumUser
from tasks.forms import EditStatusForm, TasksForm
from tasks.models import Category, Importance, Status, Task, Team, UserTeam


def get_users_in_team(team):
    user_team = UserTeam.objects.filter(ut_team=team.pk)
    # Get only users, from users and teams, and sort them alphabetically
    return sorted((itm.ut_user for itm in user_team), key=lambda k: k.username)


# def tasks_table(request):
#     tasks = Task.objects.all()
#     status = Status.objects.all()
#     context = {
#         'tasks': tasks,
#         'status': status,
#     }
#     return render(request, 'tasks/tasks_table.html', context=context)


def user_tasks_table(request):
    tasks = Task.objects.filter(tsk_user_id=request.user.pk, tsk_team_id=1)
    status = Status.objects.all()
    context = {
        'section_title': 'Your Tasks',
        'tasks': tasks,
        'status': status,
    }
    return render(request, 'tasks/tasks_table.html', context=context)


def assigned_tasks_table(request):
    pass

def create_task(request):
    user = request.user
    is_team_owner = hasattr(user, 'team_owner')

    if request.method == 'POST':
        task_form = TasksForm(request.POST)
        if task_form.is_valid():
            task = Task()
            task.tsk_name = task_form.cleaned_data['tsk_name']
            task.tsk_user = task_form.cleaned_data['tsk_user']
            task.tsk_due_date = task_form.cleaned_data['tsk_due_date']
            task.tsk_description = task_form.cleaned_data['tsk_description']
            task.tsk_category = task_form.cleaned_data['tsk_category']
            task.tsk_importance = task_form.cleaned_data['tsk_importance']
            task.tsk_status = task_form.cleaned_data['tsk_status']

            # Select task team in function of user assigned to task
            if int(task.tsk_user.pk) == int(user.pk):
                task.tsk_team = Team.objects.get(pk=1)  # Default Team
            else:
                task.tsk_team = Team.objects.get(pk=user.team_owner.pk)
            task.save()
            messages.success(request, 'Task created!')

            return redirect(reverse('user_tasks_table'))
        else:
            messages.error(request, 'Unable to create task. Please try again.')

    categories = Category.objects.all()
    importances = Importance.objects.all()
    status = Status.objects.all()
    context = {
        'user': user,
        'is_team_owner': is_team_owner,
        'categories': categories,
        'importances': importances,
        'status': status,
    }
    if is_team_owner:
        context['team_users'] = get_users_in_team(user.team_owner)

    return render(request, 'tasks/create_task.html', context=context)


def update_task(request, pk):
    user = request.user
    prev_url = HttpResponseRedirect(request.META.get('HTTP_REFERER'), '/')
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=pk)
        task_form = TasksForm(request.POST)
        if task_form.is_valid():
            task.tsk_name = task_form.cleaned_data['tsk_name']
            task.tsk_user = task_form.cleaned_data['tsk_user']
            task.tsk_due_date = task_form.cleaned_data['tsk_due_date']
            task.tsk_description = task_form.cleaned_data['tsk_description']
            task.tsk_category = task_form.cleaned_data['tsk_category']
            task.tsk_importance = task_form.cleaned_data['tsk_importance']
            task.tsk_status = task_form.cleaned_data['tsk_status']

            # Select task team in function of user assigned to task
            if int(task.tsk_user.pk) == int(user.pk):
                task.tsk_team = Team.objects.get(pk=1)  # Default Team
            else:
                task.tsk_team = Team.objects.get(pk=user.team_owner.pk)
            task.save()
            messages.success(request, 'Task updated')

            return redirect(request.POST.get('prev_url', '/'))
        else:
            messages.error(request, 'Unable to update. Please try again.')

    task = get_object_or_404(Task, pk=pk)
    is_team_owner = hasattr(user, 'team_owner')
    categories = Category.objects.all()
    importances = Importance.objects.all()
    status = Status.objects.all()
    context = {
        'task': task,
        'is_team_owner': is_team_owner,
        'categories': categories,
        'importances': importances,
        'status': status,
        'prev_url': prev_url.url,
    }
    if is_team_owner:
        context['team_users'] = get_users_in_team(user.team_owner)

    return render(request, 'tasks/update_task.html', context=context)


def update_status(request):
    task_id = request.POST['taskId']
    task = get_object_or_404(Task, pk=task_id)
    edit_status_form = EditStatusForm(request.POST)
    if edit_status_form.is_valid():
        task.tsk_status = edit_status_form.cleaned_data['tsk_status']
        task.save()
        messages.success(request, 'Status updated')
    else:
        messages.error(request, "Unable to update Status. Please try again.")
    
    prev_url = HttpResponseRedirect(request.META.get('HTTP_REFERER'), '/')

    return redirect(request.POST.get('prev_url', '/'))
