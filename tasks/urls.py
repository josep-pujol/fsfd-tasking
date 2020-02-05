from django.urls import path
from tasks.views import create_task, tasks_table, update_status, update_task

urlpatterns = [
    path('', tasks_table, name='tasks_table'),
    path('create/', create_task, name='create_task'),
    path('update/task/<int:pk>/', update_task, name='update_task'),
    path('update/status/', update_status, name='update_status'),
]
