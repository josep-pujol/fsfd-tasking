import datetime

from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from tasks.models import Status, Task
from team.models import Team, UserTeam
from tasks.views import get_users_in_team, update_status_dependencies


class UpdateStatusDependenciesHelperTest(TestCase):

    def setUp(self):
        # Create new user
        user2test = User.objects.create_user(
            username='user2test', email='usertest@email.com',
            password='XISRUkwtuK',
        )
        user2test.save()
        self.user2test = user2test

        # Create a Task
        task2test = Task.objects.create(
            tsk_user=user2test,
            tsk_name='task2test',
            tsk_description='Description of task2test',
            tsk_due_date=datetime.datetime.today().date() +
            datetime.timedelta(days=30),
        )
        task2test.save()
        self.task2test = task2test

        # Dates to assign to tasks
        self.yesters_date = datetime.datetime.today().date() - datetime.timedelta(days=1)
        self.todays_date = datetime.datetime.today().date()

    def test_status_completed_finishdate_is_today(self):
        status_completed = Status.objects.get(sta_name='completed')
        self.task2test.tsk_status = status_completed
        self.assertIsNone(self.task2test.startdate)
        update_status_dependencies(self.task2test)
        self.assertEqual(self.task2test.tsk_status, status_completed)
        self.assertEqual(self.task2test.finishdate, self.todays_date)

    def test_status_completed_finishdate_and_startdate_is_today(self):
        status_completed = Status.objects.get(sta_name='completed')
        self.task2test.tsk_status = status_completed
        self.task2test.startdate = self.yesters_date
        self.assertEqual(self.task2test.tsk_status, status_completed)
        self.assertIsNotNone(self.task2test.startdate)
        update_status_dependencies(self.task2test)
        self.assertEqual(self.task2test.finishdate, self.todays_date)
        self.assertEqual(self.task2test.startdate, self.yesters_date)

    def test_status_50_and_startdate_none_becomes_today(self):
        status_50 = Status.objects.get(sta_name='50%')
        self.task2test.tsk_status = status_50
        self.assertIsNone(self.task2test.startdate)
        self.assertEqual(self.task2test.tsk_status, status_50)
        update_status_dependencies(self.task2test)
        self.assertEqual(self.task2test.startdate, self.todays_date)

    def test_status_50_and_startdate_notnone_no_change(self):
        status_50 = Status.objects.get(sta_name='50%')
        self.task2test.tsk_status = status_50
        self.task2test.startdate = self.yesters_date
        self.assertIsNotNone(self.task2test.startdate)
        self.assertEqual(self.task2test.tsk_status, status_50)
        update_status_dependencies(self.task2test)
        self.assertEqual(self.task2test.startdate, self.yesters_date)

    def test_status_notstarted_and_startdate_none_no_change(self):
        status_notstarted = Status.objects.get(sta_name='not started')
        self.task2test.tsk_status = status_notstarted
        self.assertIsNone(self.task2test.startdate)
        self.assertEqual(self.task2test.tsk_status, status_notstarted)
        update_status_dependencies(self.task2test)
        self.assertIsNone(self.task2test.startdate)

    def test_status_notstarted_and_startdate_notnone_become_none(self):
        status_notstarted = Status.objects.get(sta_name='not started')
        self.task2test.tsk_status = status_notstarted
        self.task2test.startdate = self.yesters_date
        self.assertIsNotNone(self.task2test.startdate)
        self.assertEqual(self.task2test.tsk_status, status_notstarted)
        update_status_dependencies(self.task2test)
        self.assertIsNone(self.task2test.startdate)


class GetUsersTeamHelperTest(TestCase):

    def setUp(self):
        num_users = 5
        default_team = Team.objects.get(pk=1)
        users_list = []
        users_list.append(User.objects.get(username='admin'))
        # Create users
        for i in range(num_users):
            user2test = User.objects.create_user(
                username=f'user{i}test', email=f'user{i}test@email.com',
                password='XISRUkwtuK',
            )
            user2test.save()
            users_list.append(user2test)
            # Add user to default UserTeam
            user_team = UserTeam.objects.create(
                ut_user=user2test, ut_team=default_team)
            user_team.save()
        self.num_users = num_users + 1
        self.default_team = default_team
        self.users_list = users_list

    def test_get_users_in_team(self):
        result = get_users_in_team(self.default_team)
        self.assertEqual(result, self.users_list)


class CreateTaskViewTest(TestCase):

    @classmethod
    def setUp(cls):
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

    def test_create_task_w_default_values(self):
        # Login user
        login = self.client.login(username='user2test', password='XISRUkwtuK')
        self.assertTrue(login)
        self.assertEqual(len(Task.objects.filter(tsk_name='test_task')), 0)
        tsk_user = User.objects.get(username='user2test')
        tsk_due_date = datetime.datetime.today().date() +\
            datetime.timedelta(days=30)
        response = self.client.post(
            reverse('create_task'),
            {
                'tsk_name': 'test_task',
                'tsk_user': tsk_user.pk,
                'tsk_category': 1,
                'tsk_importance': 1,
                'tsk_status': 1,
                'tsk_due_date': tsk_due_date,
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        msgs = [msg.__str__() for msg in get_messages(response.wsgi_request)]
        self.assertIn('Task created!', msgs)
        created_task = Task.objects.filter(tsk_name='test_task')
        self.assertEqual(len(created_task), 1)


class UpdateTaskViewTest(TestCase):

    def setUp(self):
        # Create new user
        user2test = User.objects.create_user(
            username='user2test', email='usertest@email.com',
            password='XISRUkwtuK',
        )
        user2test.save()
        self.user2test = user2test

        # Create a Task
        task2test = Task.objects.create(
            tsk_user=user2test,
            tsk_name='task2test',
            tsk_description='Description of task2test',
            tsk_due_date=datetime.datetime.today().date() +
            datetime.timedelta(days=30),
        )
        task2test.save()
        self.task2test = task2test

    def test_update_task_url_exists(self):
        # Login user
        login = self.client.login(username='user2test', password='XISRUkwtuK')
        self.assertTrue(login)

        response = self.client.get(f'/tasks/update/task/{self.task2test.pk}/')
        self.assertEqual(str(response.context['user']), 'user2test')
        self.assertEqual(response.status_code, 200)

    def test_update_task_accessible_by_name(self):
        # Login user
        login = self.client.login(username='user2test', password='XISRUkwtuK')
        self.assertTrue(login)

        response = self.client.get(reverse('update_task',
                                           kwargs={'pk': self.task2test.pk}))
        self.assertEqual(str(response.context['user']), 'user2test')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        # Login user
        login = self.client.login(username='user2test', password='XISRUkwtuK')
        self.assertTrue(login)

        response = self.client.get(reverse('update_task',
                                           kwargs={'pk': self.task2test.pk}))
        self.assertEqual(str(response.context['user']), 'user2test')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/update_task.html')

    def test_view_returns_404_when_no_task_object(self):
        # Login user
        login = self.client.login(username='user2test', password='XISRUkwtuK')
        self.assertTrue(login)
        response = self.client.get('/tasks/')
        self.assertEqual(str(response.context['user']), 'user2test')

        # GET
        response = self.client.get(reverse('update_task',
                                           kwargs={'pk': 999999}))
        self.assertEqual(response.status_code, 404)

        # POST
        response = self.client.post(reverse('update_task',
                                            kwargs={'pk': 999999}))
        self.assertEqual(response.status_code, 404)

    def test_update_task_category(self):
        # Login user
        login = self.client.login(username='user2test', password='XISRUkwtuK')
        self.assertTrue(login)
        response = self.client.get(
            reverse('update_task', kwargs={'pk': f'{self.task2test.pk}'})
        )
        self.assertEqual(response.status_code, 200)
        original_task = response.context.get('task')
        self.assertEqual(original_task.tsk_category.pk, 1)
        response = self.client.post(
            reverse('update_task', kwargs={'pk': f'{self.task2test.pk}'}),
            {
                'tsk_name': original_task.tsk_name,
                'tsk_user': original_task.tsk_user.pk,
                'tsk_category': 2,
                'tsk_importance': original_task.tsk_importance.pk,
                'tsk_status': original_task.tsk_status.pk,
                'tsk_description': original_task.tsk_description,
                'tsk_due_date': original_task.tsk_due_date,
            },
            follow=True,
        )
        updated_task = Task.objects.get(pk=self.task2test.pk)
        self.assertEqual(updated_task.tsk_category.pk, 2)

    def test_update_task_importance(self):
        # Login user
        login = self.client.login(username='user2test', password='XISRUkwtuK')
        self.assertTrue(login)
        response = self.client.get(
            reverse('update_task', kwargs={'pk': f'{self.task2test.pk}'})
        )
        self.assertEqual(response.status_code, 200)
        original_task = response.context.get('task')
        self.assertEqual(original_task.tsk_importance.pk, 1)
        response = self.client.post(
            reverse('update_task', kwargs={'pk': f'{self.task2test.pk}'}),
            {
                'tsk_name': original_task.tsk_name,
                'tsk_user': original_task.tsk_user.pk,
                'tsk_category': original_task.tsk_category.pk,
                'tsk_importance': 2,
                'tsk_status': original_task.tsk_status.pk,
                'tsk_description': original_task.tsk_description,
                'tsk_due_date': original_task.tsk_due_date,
            },
            follow=True,
        )
        updated_task = Task.objects.get(pk=self.task2test.pk)
        self.assertEqual(updated_task.tsk_importance.pk, 2)

    def test_update_task_status(self):
        # Login user
        login = self.client.login(username='user2test', password='XISRUkwtuK')
        self.assertTrue(login)
        response = self.client.get(
            reverse('update_task', kwargs={'pk': f'{self.task2test.pk}'})
        )
        self.assertEqual(response.status_code, 200)
        original_task = response.context.get('task')
        self.assertEqual(original_task.tsk_status.pk, 1)
        response = self.client.post(
            reverse('update_task', kwargs={'pk': f'{self.task2test.pk}'}),
            {
                'tsk_name': original_task.tsk_name,
                'tsk_user': original_task.tsk_user.pk,
                'tsk_category': original_task.tsk_category.pk,
                'tsk_importance': original_task.tsk_importance.pk,
                'tsk_status': 2,
                'tsk_description': original_task.tsk_description,
                'tsk_due_date': original_task.tsk_due_date,
            },
            follow=True,
        )
        updated_task = Task.objects.get(pk=self.task2test.pk)
        self.assertEqual(updated_task.tsk_status.pk, 2)

    def test_update_task_due_date(self):
        # Login user
        login = self.client.login(username='user2test', password='XISRUkwtuK')
        self.assertTrue(login)
        response = self.client.get(
            reverse('update_task', kwargs={'pk': f'{self.task2test.pk}'})
        )
        self.assertEqual(response.status_code, 200)
        original_task = response.context.get('task')
        new_due_date = datetime.datetime.today().date() +\
            datetime.timedelta(days=15)
        response = self.client.post(
            reverse('update_task', kwargs={'pk': f'{self.task2test.pk}'}),
            {
                'tsk_name': original_task.tsk_name,
                'tsk_user': original_task.tsk_user.pk,
                'tsk_category': original_task.tsk_category.pk,
                'tsk_importance': original_task.tsk_importance.pk,
                'tsk_status': 2,
                'tsk_description': original_task.tsk_description,
                'tsk_due_date': new_due_date,
            },
            follow=True,
        )
        updated_task = Task.objects.get(pk=self.task2test.pk)
        self.assertEqual(updated_task.tsk_due_date, new_due_date)

    def test_update_all_fields_at_once(self):
        # Login user
        login = self.client.login(username='user2test', password='XISRUkwtuK')
        self.assertTrue(login)
        response = self.client.get(
            reverse('update_task', kwargs={'pk': f'{self.task2test.pk}'})
        )
        self.assertEqual(response.status_code, 200)
        new_due_date = datetime.datetime.today().date() +\
            datetime.timedelta(days=25)
        response = self.client.post(
            reverse('update_task', kwargs={'pk': f'{self.task2test.pk}'}),
            {
                'tsk_name': 'new_task_name',
                'tsk_user': 2,
                'tsk_category': 3,
                'tsk_importance': 3,
                'tsk_status': 3,
                'tsk_description': 'new description',
                'tsk_due_date': new_due_date,
            },
            follow=True,
        )
        updated_task = Task.objects.get(pk=self.task2test.pk)
        self.assertEqual(updated_task.tsk_name, 'new_task_name')
        self.assertEqual(updated_task.tsk_category.pk, 3)
        self.assertEqual(updated_task.tsk_importance.pk, 3)
        self.assertEqual(updated_task.tsk_status.pk, 3)
        self.assertEqual(updated_task.tsk_description, 'new description')
        self.assertEqual(updated_task.tsk_due_date, new_due_date)
