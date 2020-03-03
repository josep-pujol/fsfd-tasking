from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from team.models import Team, UserTeam


class UserTasksTableViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create new user
        user2test = User.objects.create_user(
            username='user2test', email='usertest@email.com',
            password='XISRUkwtuK',
        )
        user2test.save()

    def setUp(self):
        # Login user
        self.client.login(username='user2test', password='XISRUkwtuK')

    def test_unable_to_access_when_not_logged_in(self):
        # Logout to clear session
        self.client.logout()
        response = self.client.get('/tasks/')
        self.assertEqual(response.status_code, 302)

    def test_user_tasks_url_exists(self):
        response = self.client.get('/tasks/')
        self.assertEqual(response.status_code, 200)

    def test_user_tasks_accessible_by_name(self):
        response = self.client.get(reverse('user_tasks'))
        self.assertEqual(response.status_code, 200)

    def test_user_view_uses_correct_template(self):
        response = self.client.get(reverse('user_tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/tasks_table.html')


class AssignedTasksTableViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create new user
        user2test = User.objects.create_user(
            username='user2test', email='usertest@email.com',
            password='XISRUkwtuK',
        )
        user2test.save()

    def setUp(self):
        # Login user
        self.client.login(username='user2test', password='XISRUkwtuK')

    def test_unable_to_access_when_not_logged_in(self):
        # Logout to clear session
        self.client.logout()
        response = self.client.get('/tasks/assigned-tasks/')
        self.assertEqual(response.status_code, 302)

    def test_assigned_tasks_url_exists(self):
        response = self.client.get('/tasks/assigned-tasks/')
        self.assertEqual(response.status_code, 200)

    def test_assigned_tasks_accessible_by_name(self):
        response = self.client.get(reverse('assigned_tasks'))
        self.assertEqual(response.status_code, 200)

    def test_assigned_view_uses_correct_template(self):
        response = self.client.get(reverse('assigned_tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/tasks_table.html')

    def test_assigned_view_uses_right_template_and_section_title(self):
        response = self.client.get(reverse('assigned_tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/tasks_table.html')
        self.assertContains(response, 'Assigned Tasks')


class TeamTasksTableViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create new user
        user2test = User.objects.create_user(
            username='user2test', email='usertest@email.com',
            password='XISRUkwtuK',
        )
        user2test.save()

        # Create a Team and premium user
        team = Team.objects.create(
            tem_name=f"{user2test.username}'s Team",
            tem_description='Team managed by user '
                            f'{user2test.username}',
            tem_owner=user2test,
        )
        team.save()

        # Create relationship User Team for premium user
        user_team = UserTeam.objects.create(
            ut_user=user2test,
            ut_team=team,
        )
        user_team.save()

    def setUp(self):
        # Login user
        self.client.login(username='user2test', password='XISRUkwtuK')

    def test_unable_to_access_when_not_logged_in(self):
        # Logout to clear session
        self.client.logout()
        response = self.client.get('/tasks/team-tasks/')
        self.assertEqual(response.status_code, 302)

    def test_team_tasks_url_exists(self):
        response = self.client.get('/tasks/team-tasks/')
        self.assertEqual(response.status_code, 200)

    def test_team_tasks_accessible_by_name(self):
        response = self.client.get(reverse('team_tasks'))
        self.assertEqual(response.status_code, 200)

    def test_team_view_uses_correct_template(self):
        response = self.client.get(reverse('team_tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/tasks_table.html')

    def test_team_view_uses_right_template_and_section_title(self):
        response = self.client.get(reverse('team_tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/tasks_table.html')
        self.assertContains(response, 'Team&#39;s Task List')


class CompletedTasksTableViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create new user
        user2test = User.objects.create_user(
            username='user2test', email='usertest@email.com',
            password='XISRUkwtuK',
        )
        user2test.save()

    def setUp(self):
        # Login user
        self.client.login(username='user2test', password='XISRUkwtuK')

    def test_unable_to_access_when_not_logged_in(self):
        # Logout to clear session
        self.client.logout()
        response = self.client.get('/tasks/completed-tasks/')
        self.assertEqual(response.status_code, 302)

    def test_completed_tasks_url_exists(self):
        response = self.client.get('/tasks/completed-tasks/')
        self.assertEqual(response.status_code, 200)

    def test_completed_tasks_accessible_by_name(self):
        response = self.client.get(reverse('completed_tasks'))
        self.assertEqual(response.status_code, 200)

    def test_completed_view_uses_correct_template(self):
        response = self.client.get(reverse('completed_tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/completed_tasks_table.html')

    def test_completed_view_uses_right_template_and_section_title(self):
        response = self.client.get(reverse('completed_tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/completed_tasks_table.html')
        self.assertContains(response, 'Completed Tasks')
