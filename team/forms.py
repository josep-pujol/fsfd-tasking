from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class AddCollaboratorForm(forms.Form):
    """Form used to add a collaborator in team"""

    email_to_add = forms.EmailField(
        label='An email from a Tasking user',
        widget=forms.EmailInput(),
    )

    def clean_email_to_add(self):
        email_ = self.cleaned_data['email_to_add']

        try:
            User.objects.get(email=email_)
            return email_
        except Exception as e:
            print(e)
            raise forms.ValidationError(
                'This email is not registered.'
                'The email owner needs to register to Tasking first.'
            )
