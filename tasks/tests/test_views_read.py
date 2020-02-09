import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from tasks.models import Category, Importance, Status, Task


class UserTasksTableViewTest(TestCase):

    @classmethod
    def setUp(self):
        # Create new user
        user2test = User.objects.create_user(
            username='user2test', email='usertest@email.com',
            password='XISRUkwtuK',
        )
        user2test.save()

    def test_user_tasks_table_url_exists(self):
        # Login user
        login = self.client.login(username='user2test', password='XISRUkwtuK')
        self.assertTrue(login)

        response = self.client.get('/tasks/')
        self.assertEqual(str(response.context['user']), 'user2test')
        self.assertEqual(response.status_code, 200)

    def test_user_tasks_table_accessible_by_name(self):
        # Login user
        login = self.client.login(username='user2test', password='XISRUkwtuK')
        self.assertTrue(login)

        response = self.client.get(reverse('user_tasks_table'))
        self.assertEqual(str(response.context['user']), 'user2test')
        self.assertEqual(response.status_code, 200)

    def test_user_view_uses_correct_template(self):
        # Login user
        login = self.client.login(username='user2test', password='XISRUkwtuK')
        self.assertTrue(login)

        response = self.client.get(reverse('user_tasks_table'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/tasks_table.html')


class AssignedTasksTableViewTest(TestCase):

    @classmethod
    def setUp(self):
        # Create new user
        user2test = User.objects.create_user(
            username='user2test', email='usertest@email.com',
            password='XISRUkwtuK',
        )
        user2test.save()

    def test_assigned_tasks_table_url_exists(self):
        # Login user
        login = self.client.login(username='user2test', password='XISRUkwtuK')
        self.assertTrue(login)

        response = self.client.get('/tasks/assigned-tasks/')
        self.assertEqual(str(response.context['user']), 'user2test')
        self.assertEqual(response.status_code, 200)

    def test_assigned_tasks_table_accessible_by_name(self):
        # Login user
        login = self.client.login(username='user2test', password='XISRUkwtuK')
        self.assertTrue(login)

        response = self.client.get(reverse('assigned_tasks_table'))
        self.assertEqual(str(response.context['user']), 'user2test')
        self.assertEqual(response.status_code, 200)

    def test_assigned_view_uses_correct_template(self):
        # Login user
        login = self.client.login(username='user2test', password='XISRUkwtuK')
        self.assertTrue(login)

        response = self.client.get(reverse('assigned_tasks_table'))
        self.assertEqual(str(response.context['user']), 'user2test')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/tasks_table.html')
