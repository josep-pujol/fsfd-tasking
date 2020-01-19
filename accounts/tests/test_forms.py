from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class UserRegistrationFormTest(TestCase):
    @classmethod
    def setUp(self):
        print('\n\nsetup')
        user2test = User.objects.create_user(
            username='user2test', email='user2_test@email.com',
            password1='1X<ISRUkw+tuK', password2='1X<ISRUkw+tuK',
        )
        user2test.save()
        print(user2test)

    def test_email_address_already_registered(self):
        # Raise validation error when Email address is already
        # registered
        print('\n\ntest')
        response = self.client.post(
            reverse('/register/'),
            {
             'username': 'user', 'email': 'user2_test@email.com',
             'password1': '1X<ISRUkw+tuK', 'password2': '1X<ISRUkw+tuK',
             }
        )
        print(response)
        self.assertFormError(
            response, 'registration_form', 'email',
            'This email address is already in use'
        ) 