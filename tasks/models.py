from django.db import models
from django.contrib.auth.models import User
from django.db.models import F, Q

from team.models import Team


class Category(models.Model):
    cat_name = models.CharField(max_length=200)
    cat_description = models.TextField()
    cat_order = models.PositiveIntegerField()

    class Meta:
        ordering = ['cat_order', ]

    def __str__(self):
        return self.cat_name


class Importance(models.Model):
    imp_name = models.CharField(max_length=200)
    imp_description = models.TextField()
    imp_order = models.PositiveIntegerField()

    class Meta:
        ordering = ['imp_order', ]

    def __str__(self):
        return self.imp_name


class Status(models.Model):
    sta_name = models.CharField(max_length=200)
    sta_description = models.TextField()
    sta_order = models.PositiveIntegerField()

    class Meta:
        ordering = ['sta_order', ]

    def __str__(self):
        return self.sta_name


class Task(models.Model):
    tsk_user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    tsk_team = models.ForeignKey(
        Team, on_delete=models.CASCADE, blank=True, null=True, default=1)  # default Tasking team
    tsk_category = models.ForeignKey(
        Category, on_delete=models.CASCADE, default=1)  # default Undefined
    tsk_status = models.ForeignKey(
        Status, on_delete=models.CASCADE, default=1)  # default Not started
    tsk_importance = models.ForeignKey(
        Importance, on_delete=models.CASCADE, default=1)  # default Low
    tsk_name = models.CharField(max_length=200)
    tsk_description = models.TextField(blank=True, null=True)
    tsk_due_date = models.DateField()
    startdate = models.DateField(blank=True, null=True)
    finishdate = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['tsk_due_date', ]
        constraints = [
            models.CheckConstraint(
                check=Q(startdate__lte=F('finishdate')),
                name='startdate_lte_finishdate',
            ),
        ]

    def __str__(self):
        return str((self.pk, self.tsk_name))
