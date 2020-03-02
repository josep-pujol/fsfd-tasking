from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from team.models import Team, UserTeam


class UserTeamViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create test users
        user2test = User.objects.create_user(
            username='user2test', email='usertest@email.com',
            password='XISRUkwtuK',
        )
        user2test.save()

        user2test_B = User.objects.create_user(
            username='user2test_B', email='usertest_B@email.com',
            password='XISRUkwtuK',
        )
        user2test_B.save()

        # Create a Team and premium user for user2test
        team = Team.objects.create(
            tem_name=f"{user2test.username}'s Team",
            tem_description='Team managed by user '
                            f'{user2test.username}',
            tem_owner=user2test,
        )
        team.save()

        # Create relationship User Team for premium user/user2test
        user_team = UserTeam.objects.create(
            ut_user=user2test,
            ut_team=team,
        )
        user_team.save()

    def setUp(self):
        # Login user
        self.client.login(username='user2test', password='XISRUkwtuK')

    def test_collaborators_url_exists(self):
        response = self.client.get('/team/collaborators/')
        self.assertEqual(response.status_code, 200)

    def test_add_collaborators_url_exists(self):
        response = self.client.get('/team/collaborators/add/')
        self.assertEqual(response.status_code, 200)

    def test_collaborators_url_accessible_by_name(self):
        response = self.client.get(reverse('team_collaborators'))
        self.assertEqual(response.status_code, 200)

    def test_add_collaborators_url_accessible_by_name(self):
        response = self.client.get(reverse('add_collaborator'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        # Team Collaborators url
        response_team = self.client.get(reverse('team_collaborators'))
        # Add Collaborator url
        response_add = self.client.get(reverse('add_collaborator'))
        self.assertEqual(response_team.status_code, 200)
        self.assertTemplateUsed(response_team, 'team/team_collaborators.html')
        self.assertEqual(response_add.status_code, 200)
        self.assertTemplateUsed(response_add, 'team/team_collaborators.html')

    def test_premium_user_can_add_registered_user_to_team(self):
        response = self.client.post(reverse('add_collaborator'),
                                    {'email_to_add': 'usertest_B@email.com'},
                                    follow=True)
        msgs = [msg.__str__() for msg in get_messages(response.wsgi_request)]
        premium_user = User.objects.get(email='usertest@email.com')
        user_added2team = User.objects.get(email='usertest_B@email.com')
        user_team = UserTeam.objects.get(
            ut_team=premium_user.team_owner.pk, ut_user=user_added2team.pk)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Added to your Team!', msgs)
        self.assertEqual('usertest_B@email.com', user_team.ut_user.email)

    def test_premium_user_get_error_msg_if_adding_existing_team_user(self):
        # Add Team user
        response = self.client.post(reverse('add_collaborator'),
                                    {'email_to_add': 'usertest_B@email.com'},
                                    follow=True)
        premium_user = User.objects.get(email='usertest@email.com')
        user_added2team = User.objects.get(email='usertest_B@email.com')
        user_team = UserTeam.objects.get(
            ut_team=premium_user.team_owner.pk, ut_user=user_added2team.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual('usertest_B@email.com', user_team.ut_user.email)

        # Try a second time to get error
        response = self.client.post(reverse('add_collaborator'),
                                    {'email_to_add': 'usertest_B@email.com'},
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        msgs = [msg.__str__() for msg in get_messages(response.wsgi_request)]
        self.assertIn(
            'usertest_B@email.com is already a Collaborator in the Team', msgs)

    def test_premium_user_gets_error_when_adding_unregistered_user(self):
        response = self.client.post(
            reverse('add_collaborator'),
            {'email_to_add': 'not_registered@email.com'},
            follow=True
        )
        msgs = [msg.__str__() for msg in get_messages(response.wsgi_request)]
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            'Please ensure the email belongs to a Tasking user', msgs)

    def test_user_redirected_when_not_logged_or_unknown_user(self):
        # Clear session logging out user
        self.client.logout()
        # Trying to Login unkwnow user
        login = self.client.login(
            username='testuser_unknown', password='XISRUkwtuK')
        response = self.client.get(reverse('team_collaborators'), follow=True)
        self.assertFalse(login)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(
            response, '/accounts/login/?next=/team/collaborators/')
