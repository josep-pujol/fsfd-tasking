from django import forms
from tasks.models import Task


class TasksForm(forms.ModelForm):
    """Form used to create and update a Task"""
    class Meta:
        model = Task
        fields = '__all__'


class EditStatusForm(forms.ModelForm):
    """Form used to update Status"""
    class Meta:
        model = Task
        fields = ['tsk_status', ]
