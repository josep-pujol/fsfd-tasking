from django.contrib.auth.models import User
from django.db import models


class Team(models.Model):
    """Info about Teams"""
    tem_name = models.CharField(max_length=200)
    tem_description = models.TextField()
    tem_owner = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='team_owner',
    )

    def __str__(self):
        return self.tem_name


class UserTeam(models.Model):
    """Relationship User Team"""
    ut_user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    ut_team = models.ForeignKey(
        Team, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        ordering = ['ut_team', ]
        constraints = [
            models.UniqueConstraint(
                fields=['ut_user', 'ut_team', ],
                name='user_team'
            )
        ]

    def __str__(self):
        return str((self.ut_team, self.ut_user))
