from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy

from subscriptions.models import PremiumUser
from tasks.forms import EditStatusForm, TasksForm
from tasks.models import Category, Importance, Status, Task, Team, UserTeam


def tasks_table(request):
    tasks = Task.objects.all()
    status = Status.objects.all()
    context = {
        'tasks': tasks,
        'status': status,
    }
    return render(request, 'tasks/tasks_table.html', context=context)


def create_task(request):
    user = request.user
    print(user)
    is_team_owner = hasattr(user, 'team_owner')

    if request.method == 'POST':
        # TODO toast message
        task_form = TasksForm(request.POST)
        print(request.POST)
        if task_form.is_valid():
            task = Task()
            task.tsk_name = task_form.cleaned_data['tsk_name']
            task.tsk_due_date = task_form.cleaned_data['tsk_due_date']
            task.tsk_description = task_form.cleaned_data['tsk_description']
            task.tsk_category = task_form.cleaned_data['tsk_category']
            task.tsk_importance = task_form.cleaned_data['tsk_importance']
            task.tsk_status = task_form.cleaned_data['tsk_status']
            task.save()
            messages.success(request, 'Task created!')
            return redirect(reverse('tasks_table'))
        else:
            messages.error(request, 'Unable to create task. Please try again.')

    team = Team.objects.get(pk=1)  # Default team
    categories = Category.objects.all()
    importances = Importance.objects.all()
    status = Status.objects.all()
    context = {
        'user': user,
        'is_team_owner': is_team_owner,
        'team': team,
        'categories': categories,
        'importances': importances,
        'status': status,
    }
    if is_team_owner:
        user_team = UserTeam.objects.filter(ut_team=user.team_owner.pk)
        # Get only users and sort them alphabetically
        team_users = sorted((itm.ut_user for itm in user_team),
                            key=lambda k: k.username)
        context['team_users'] = team_users
    print(context)

    return render(request, 'tasks/create_task.html', context=context)


def update_task(request, pk):
    if request.method == 'POST':
        # TODO user & toast message
        task = get_object_or_404(Task, pk=pk)
        task_form = TasksForm(request.POST)
        if task_form.is_valid():
            task.tsk_name = task_form.cleaned_data['tsk_name']
            task.tsk_due_date = task_form.cleaned_data['tsk_due_date']
            task.tsk_description = task_form.cleaned_data['tsk_description']
            task.tsk_category = task_form.cleaned_data['tsk_category']
            task.tsk_importance = task_form.cleaned_data['tsk_importance']
            task.tsk_status = task_form.cleaned_data['tsk_status']
            task.save()
            print(messages.get_level(request))
            messages.success(request, 'Task updated')
            return redirect(reverse('tasks_table'))
        else:
            messages.error(request, 'Unable to update. Please try again.')
    # TODO user
    task = get_object_or_404(Task, pk=pk)
    categories = Category.objects.all()
    importances = Importance.objects.all()
    status = Status.objects.all()
    context = {
        'task': task,
        'categories': categories,
        'importances': importances,
        'status': status,
    }
    return render(request, 'tasks/update_task.html', context=context)


def update_status(request):
    task_id = request.POST['taskId']
    task = get_object_or_404(Task, pk=task_id)
    edit_status_form = EditStatusForm(request.POST)
    if edit_status_form.is_valid():
        task.tsk_status = edit_status_form.cleaned_data['tsk_status']
        task.save()
    return redirect(reverse('tasks_table'))
    # TODO toast message to confirm or reject?
    # else:
    #     messages.error(request, "unable to log you in at this time!")
