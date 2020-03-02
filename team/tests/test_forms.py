from django.contrib.auth.models import User
from django.test import TestCase

from team.forms import AddCollaboratorForm


class AddCollaboratorFormTest(TestCase):

    def test_invalid_email_return_invalid_form(self):
        invalid_emails = ['email.invalid.com', 'aa', '@adf.com', ]
        for email in invalid_emails:
            form = AddCollaboratorForm(data={'email_to_add': email})
            self.assertFalse(form.is_valid())

    def test_valid_unregistered_email_returns_invalid_form(self):
        valid_unregistered_email = 'user_unregistered_test@email.com'
        form = AddCollaboratorForm(
            data={'email_to_add': valid_unregistered_email})
        self.assertFalse(form.is_valid())

    def test_valid_registered_email_return_valid_form(self):
        # Create new user
        user2test = User.objects.create_user(
            username='user2test', email='usertest@email.com',
            password='XISRUkwtuK',
        )
        user2test.save()

        valid_email = user2test.email
        form = AddCollaboratorForm(data={'email_to_add': valid_email})
        self.assertTrue(form.is_valid())
