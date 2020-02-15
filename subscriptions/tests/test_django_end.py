from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from tasks.models import Team, UserTeam


class SubscriptionsViewTest(TestCase):

    @classmethod
    def setUp(self):
        # Create new user
        user2test = User.objects.create_user(
            username='user2test', email='usertest@email.com',
            password='XISRUkwtuK',
        )
        user2test.save()
        self.user2test = user2test

    def test_unable_to_access_unless_logged_in(self):
        response = self.client.get('/subscriptions/')
        self.assertEqual(response.status_code, 302)

    def test_subscriptions_url_exists(self):
        # Login user
        login = self.client.login(username='user2test', password='XISRUkwtuK')
        self.assertTrue(login)

        response = self.client.get('/subscriptions/')
        self.assertEqual(str(response.context['user']), 'user2test')
        self.assertEqual(response.status_code, 200)

    def test_subscriptions_accessible_by_name(self):
        # Login user
        login = self.client.login(username='user2test', password='XISRUkwtuK')
        self.assertTrue(login)

        response = self.client.get(reverse('subscribe'))
        self.assertEqual(str(response.context['user']), 'user2test')
        self.assertEqual(response.status_code, 200)

    def test_subscriptions_uses_correct_template(self):
        # Login user
        login = self.client.login(username='user2test', password='XISRUkwtuK')
        self.assertTrue(login)

        response = self.client.get(reverse('subscribe'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'subscriptions/subscribe.html')
        self.assertContains(response, 'START COLLABORATING')

    def test_redirected_to_login_page_if_not_logged_in(self):
        response = self.client.get('/subscriptions/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertURLEqual(response.request['PATH_INFO'], reverse('login'))
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_redirected_to_subscriptions_if_logged_in_not_premium(self):
        # Login user
        login = self.client.login(username='user2test', password='XISRUkwtuK')
        self.assertTrue(login)

        response = self.client.get('/accounts/login/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertURLEqual(response.request['PATH_INFO'], reverse('subscribe'))
        self.assertTemplateUsed(response, 'subscriptions/subscribe.html')

    def test_redirected_to_user_tasks_if_logged_in_and_team_owner(self):
        # Login user
        login = self.client.login(username='user2test', password='XISRUkwtuK')
        self.assertTrue(login)

        # Create a Team and premium user
        # user2test = User.objects.filter(username='user2test')
        team = Team.objects.create(
            tem_name=f"{self.user2test.username.capitalize()}'s Team",
            tem_description='Team managed by user '
                            f'{self.user2test.username.capitalize()}',
            tem_owner=self.user2test,
        )
        team.save()

        # Create relationship User Team for premium user
        user_team = UserTeam.objects.create(
            ut_user=self.user2test,
            ut_team=team,
        )
        user_team.save()

        response = self.client.get('/accounts/login/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertURLEqual(
            response.request['PATH_INFO'], reverse('user_tasks'))
        self.assertTemplateUsed(response, 'tasks/tasks_table.html')
