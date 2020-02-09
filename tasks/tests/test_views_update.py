import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from tasks.models import Category, Importance, Status, Task


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
            tsk_due_date=datetime.datetime.today() + datetime.timedelta(days=30),
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
    #     response = self.client.get(f'/tasks/update/task/{self.task2test.pk}/')
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
