from django.shortcuts import render


def task_list(request):
    """Return the task_list.html file"""
    return render(request, 'tasks/tasks_table.html')
