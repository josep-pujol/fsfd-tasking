from django import forms
from django.contrib.auth.models import User

from tasks.models import UserTeam


class AddCollaboratorForm(forms.Form):
    """Form used to add a collaborator in team"""

    email_to_add = forms.EmailField(
        label='Email',
        widget=forms.TextInput(
            attrs={'placeholder': 'Email from a Tasking user'},
        )
    )

    def clean_email(self):
        email_ = self.cleaned_data['email_to_add']

        if User.objects.filter(email=email_):
            return email_

        raise forms.ValidationError(
            u'This email is not registered. '
            u'The email owner needs to register to Tasking first.'
        )
