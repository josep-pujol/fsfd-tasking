import re
from io import StringIO

from django.apps import AppConfig
from django.core.management import call_command
from django.db import connection
from django.db.models.signals import post_migrate


def reset_sequences(sender, **kwargs):
    """ reset the sql sequences """
    print('reset_sequences')

    # list of apps to reset 
    app_names = ['tasks', ]

    for app_name in app_names:
        output = StringIO()
        call_command('sqlsequencereset', app_name, stdout=output)
        sql = output.getvalue()

        # Remove terminal color codes from sqlsequencereset output
        ansi_escape = re.compile(r'\x1b[^m]*m')
        sql = ansi_escape.sub('', sql)

        with connection.cursor() as cursor:
            cursor.execute(sql)


class TasksConfig(AppConfig):
    name = 'tasks'

    def ready(self):
        post_migrate.connect(reset_sequences, sender=self)
