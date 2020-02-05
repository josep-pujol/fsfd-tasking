from django.shortcuts import render


def tasks_table(request):
    """Return the task_list.html file"""
    return render(request, 'tasks/tasks_table.html')

def create_task(request):
    pass

def update_task(request, pk):
    pass

def update_status(request):
    pass
