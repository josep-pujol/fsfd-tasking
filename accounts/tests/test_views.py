from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User


class LoginViewTest(TestCase):
    @classmethod
    def setUp(self):
        # Create new user
        user2test = User.objects.create_user(
            username='user2test', email='usertest@email.com',
            password='XISRUkwtuK',
        )
        user2test.save()

    def test_accounts_login_url_exists(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_unkwnow_user_unable_to_login(self):
        # Trying to Login unkwnow user
        login = self.client.login(
            username='testuser_unknown', password='XISRUkwtuK')
        self.assertFalse(login)

    def test_known_user_wrong_pwd_unable_to_login(self):
        # Trying to Login know user with wrong password
        login = self.client.login(
            username='user2test', password='1')
        self.assertFalse(login)

    def test_correct_login_details_able_to_login(self):
        login = self.client.login(
            username='user2test', password='XISRUkwtuK')
        self.assertTrue(login)

    def test_correct_user_logged_in_and_in_session(self):
        login = self.client.login(
            username='user2test', password='XISRUkwtuK')
        user = User.objects.filter(username='user2test')
        self.assertTrue(login)
        self.assertEqual(int(self.client.session['_auth_user_id']), 
                         user[0].id)

    def test_redirect_to_tasklist_if_logged_in(self):
        # Login user
        login = self.client.login(
            username='user2test', password='XISRUkwtuK')
        self.assertTrue(login)
        # Requesting the login page should redirect to index
        response = self.client.get('/accounts/login/', follow=True)
        task_list_response = self.client.get(reverse('task_list'))
        self.assertRedirects(response, '/tasks/')
        self.assertEqual(response.content, task_list_response.content)


class LogoutViewTest(TestCase):
    @classmethod
    def setUp(self):
        # Create new user
        user2test = User.objects.create_user(
            username='user2test', email='usertest@email.com',
            password='XISRUkwtuK',
        )
        user2test.save()

    def test_logout_view_logs_out_user(self):
        login = self.client.login(
            username='user2test', password='XISRUkwtuK')
        self.assertTrue(login)
        user = User.objects.filter(username='user2test')
        response = self.client.get('/accounts/logout/', follow=True)
        self.assertEqual(response.status_code, 200)
        try:
            self.client.session['_auth_user_id']
            self.assertNotEqual(int(self.client.session['_auth_user_id']), 
                                user[0].id)
        except KeyError as exc:
            self.assertEqual(repr(exc), "KeyError('_auth_user_id')")

    def test_view_url_accessible_by_name(self):
        login = self.client.login(
            username='user2test', password='XISRUkwtuK')
        self.assertTrue(login)
        response = self.client.get(reverse('logout'), follow=False)
        self.assertEqual(response.status_code, 302)

    def test_view_uses_correct_template(self):
        login = self.client.login(
            username='user2test', password='XISRUkwtuK')
        self.assertTrue(login)
        response = self.client.get(reverse('logout'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/index.html')

    def test_redirect_to_index_when_logging_out(self):
        # Login user
        login = self.client.login(
            username='user2test', password='XISRUkwtuK')
        self.assertTrue(login)

        # Logout url should logout user and redirect to index
        response = self.client.get('/accounts/logout/', follow=True)
        self.assertRedirects(response, '/')
