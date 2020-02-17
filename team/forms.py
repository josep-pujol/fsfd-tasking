from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class AddCollaboratorForm(forms.Form):
    """Form used to add a collaborator in team"""

    email_to_add = forms.EmailField(
        label='Email',
        widget=forms.TextInput(
            attrs={'placeholder': 'Email from a Tasking user'},
        )
    )

    def clean_email_to_add(self):
        email_ = self.cleaned_data['email_to_add']

        try:
            User.objects.get(email=email_)
            return email_
        except Exception as e:
            print(e)
            raise ValidationError(
                u'This email is not registered. '
                u'The email owner needs to register to Tasking first.'
            )
