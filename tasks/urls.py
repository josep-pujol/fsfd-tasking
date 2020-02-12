from django.urls import path
from tasks.views import (
    assigned_tasks, completed_tasks, create_task,
    team_tasks, user_tasks, update_status, update_task
)


urlpatterns = [
    path('', user_tasks, name='user_tasks'),
    path('assigned-tasks/', assigned_tasks, name='assigned_tasks'),
    path('completed-tasks/', completed_tasks, name='completed_tasks'),
    path('team-tasks/', team_tasks, name='team_tasks'),
    path('create/', create_task, name='create_task'),
    path('update/task/<int:pk>/', update_task, name='update_task'),
    path('update/status/', update_status, name='update_status'),
]
