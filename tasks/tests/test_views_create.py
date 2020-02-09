import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from tasks.models import Category, Importance, Status, Task


class CreateTaskViewTest(TestCase):

    @classmethod
    def setUp(self):
        # Create new user
        user2test = User.objects.create_user(
            username='user2test', email='usertest@email.com',
            password='XISRUkwtuK',
        )
        user2test.save()

    def test_create_task_url_exists(self):
        # Login user
        login = self.client.login(username='user2test', password='XISRUkwtuK')
        self.assertTrue(login)

        response = self.client.get('/tasks/create/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'user2test')

    def test_create_task_accessible_by_name(self):
        # Login user
        login = self.client.login(username='user2test', password='XISRUkwtuK')
        self.assertTrue(login)

        response = self.client.get(reverse('create_task'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'user2test')

    def test_view_uses_correct_template(self):
        # Login user
        login = self.client.login(username='user2test', password='XISRUkwtuK')
        self.assertTrue(login)

        response = self.client.get(reverse('create_task'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'user2test')
        self.assertTemplateUsed(response, 'tasks/create_task.html')
