from django.contrib.auth.models import User
from django.test import TestCase

from accounts.backends import EmailAuth


class UpdateTaskViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create new user
        user2test = User.objects.create_user(
            username='user2test', email='usertest@email.com',
            password='XISRUkwtuK',
        )
        user2test.save()

    def test_no_user_match_no_password_return_none(self):
        res = EmailAuth.authenticate(self, request=None, username='auser')
        self.assertIsNone(res)

    def test_no_email_match_no_password_return_none(self):
        res = EmailAuth.authenticate(
            self, request=None, username='auser@email.com')
        self.assertIsNone(res)

    def test_user_match_no_password_return_none(self):
        res = EmailAuth.authenticate(
            self, request=None, username='usertest@email.com')
        self.assertIsNone(res)

    def test_email_match_no_password_return_none(self):
        res = EmailAuth.authenticate(
            self, request=None, username='usertest@email.com')
        self.assertIsNone(res)

    def test_user_match_with_password_return_user(self):
        user = User.objects.get(email='usertest@email.com')
        res = EmailAuth.authenticate(
            self,
            request=None,
            username='usertest@email.com',
            password='XISRUkwtuK',
        )
        self.assertEqual(res, user)

    def test_email_match_with_password_return_user(self):
        user = User.objects.get(email='usertest@email.com')
        res = EmailAuth.authenticate(
            self,
            request=None,
            username='usertest@email.com',
            password='XISRUkwtuK',
        )
        self.assertEqual(res, user)

    def test_user_do_not_exist_return_none(self):
        res = EmailAuth.get_user(self, user_id=99999999999999999)
        self.assertIsNone(res)

    def test_user_exist_return_user(self):
        user = User.objects.get(email='usertest@email.com')
        res = EmailAuth.get_user(self, user_id=user.pk)
        self.assertEqual(res, user)
