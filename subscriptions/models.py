from django.db import models
from django.contrib.auth.models import User


class PremiumUser(models.Model):
    """Extend Django User model with information about Stripe subscriptions"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=255)
    stripe_subscription_id = models.CharField(max_length=255)
    subscription_date = models.DateField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return f"{self.user}-{self.stripe_id}-{self.stripe_subscription_id}"
