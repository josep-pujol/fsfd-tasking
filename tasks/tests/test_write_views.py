import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from tasks.models import Category, Importance, Status, Task
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
            tsk_due_date=datetime.datetime.today() +
            datetime.timedelta(days=30),
        )
        task2test.save()
        self.task2test = task2test

        # Dates to assign to tasks
        self.yesters_date = datetime.datetime.today() - datetime.timedelta(days=1)
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


# class GetUsersTeamsHelperTest(TestCase):

#     def setUp(self):
#         # Create new user
#         user2test = User.objects.create_user(
#             username='user2test', email='usertest@email.com',
#             password='XISRUkwtuK',
#         )
#         user2test.save()
#         self.user2test = user2test


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


class UpdateTaskViewTest(TestCase):

    @classmethod
    def setUp(self):
        # Create new user
        user2test = User.objects.create_user(
            username='user2test', email='usertest@email.com',
            password='XISRUkwtuK',
        )
        user2test.save()

        # Create Categories
        cat2test1 = Category.objects.create(cat_name='Undefined', cat_order=1)
        cat2test1.save()
        cat2test2 = Category.objects.create(cat_name='Admin', cat_order=2)
        cat2test2.save()
        cat2test3 = Category.objects.create(cat_name='Other', cat_order=3)
        cat2test3.save()

        # Create Importances
        imp2test1 = Importance.objects.create(imp_name='High', imp_order=3)
        imp2test1.save()
        imp2test2 = Importance.objects.create(imp_name='Medium', imp_order=2)
        imp2test2.save()
        imp2test3 = Importance.objects.create(imp_name='Low', imp_order=1)
        imp2test3.save()

        # Create Status
        sta2test1 = Status.objects.create(sta_name='Not Started', sta_order=1)
        sta2test1.save()
        sta2test2 = Status.objects.create(sta_name='50%', sta_order=2)
        sta2test2.save()
        sta2test3 = Status.objects.create(sta_name='Completed', sta_order=3)
        sta2test3.save()

        # Create a Task
        self.task2test = Task.objects.create(
            tsk_user=user2test,
            tsk_category=cat2test1,
            tsk_importance=imp2test2,
            tsk_status=sta2test3,
            tsk_name='task2test',
            tsk_description='Description of task2test',
            tsk_due_date=datetime.datetime.today() +
            datetime.timedelta(days=30),
        )

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






    # def test_updates_category(self):
    #     response = self.client.get(
    #       things'/tasks/update/task/{self.task2test.pk}/')
    #     self.assertEqual(response.status_code, 200)
    #     from pprint import pprint as pp
    #     print('\nCONTEXT')
    #     pp(response.context)
    #     print(dir(response))
    #     print(response.context.get('task').id)
    #     print(response.context.get('task').pk)
    #     print(response.context.get('task').tsk_category_id)
    #     print(response.context.get('task').tsk_category)
    #     task = response.context.get('task')
    #     task.tsk_category = Category.objects.get(pk=2)
    #     print(type(task))
    #     print(dir(task))
    #     print(task.tsk_name)
    #     response = self.client.post(
    #         f'/tasks/update/task/{self.task2test.pk}/',
    #         {'task': task}
    #     )
    #     print('RESPONSE', response)
    #     self.assertEqual(response.status_code, 200)

    # def test_updates_category(self):
    #     response = self.client.post(
    #         f'/tasks/update/task/{self.task2test.pk}/',
    #         {'task': task}
    #     )
    #     from pprint import pprint as pp
    #     print('\nCONTEXT')
    #     pp(response.context)
    #     print(dir(response))
    #     print(response.context.get('task').id)
    #     print(response.context.get('task').pk)
    #     print(response.context.get('task').tsk_category_id)
    #     print(response.context.get('task').tsk_category)
    #     task = response.context.get('task')
    #     task.tsk_category = Category.objects.get(pk=2)
    #     print(type(task))
    #     print(dir(task))
    #     print(task.tsk_name)

    #     print('RESPONSE', response)
    #     self.assertEqual(response.status_code, 200)
