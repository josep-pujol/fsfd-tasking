from django.contrib.auth.models import User
from django.test import TestCase


class UserRegistrationFormTest(TestCase):
    @classmethod
    def setUp(self):
        user2test = User.objects.create_user(
            username='user2test', email='usertest@email.com',
            password='XISRUkwtuK',
        )
        user2test.save()

    def test_username__already_registered(self):
        # Raise validation error when trying to register a username
        # that is already in use
        response = self.client.post(
            '/accounts/register/',
            {
             'username': 'user', 'email': 'usertest@email.com',
             'password': 'XISRUkwtuK',
             }
        )
        self.assertFormError(
            response, 'registration_form', 'email',
            'This email address is already in use'
        )

    def test_email_address_already_registered(self):
        # Raise validation error when trying to register an email
        # address that is already in use
        response = self.client.post(
            '/accounts/register/',
            {
             'username': 'user2test', 'email': 'user2test@email.com',
             'password': 'XISRUkwtuK',
             }
        )
        self.assertFormError(
            response, 'registration_form', 'username',
            'A user with that username already exists.'
        )
