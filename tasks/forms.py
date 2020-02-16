from django import forms
from tasks.models import Task


class TasksForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'


class EditStatusForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['tsk_status', ]
