from django.urls import path
from tasks.views import (assigned_tasks_table, create_task, user_tasks_table,
                         update_status, update_task)


urlpatterns = [
    path('', user_tasks_table, name='user_tasks_table'),
    path('assigned-tasks/', assigned_tasks_table, name='assigned_tasks_table'),
    path('create/', create_task, name='create_task'),
    path('update/task/<int:pk>/', update_task, name='update_task'),
    path('update/status/', update_status, name='update_status'),
]
