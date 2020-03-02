import os

from django.contrib.auth.models import User
from django.test import TestCase

import stripe
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')


class StripeApiTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create new Application user
        user2test = User.objects.create_user(
            username='user2test', email='usertest@email.com',
            password='XISRUkwtuK',
        )
        user2test.save()
        cls.user2test = user2test

        # Create new Stripe Customer
        cls.email = "user2test_stripe@gmail.com"
        cls.description = "customer for user2test_stripe"
        cls.stripe_customer = stripe.Customer.create(
            email=cls.email,
            description=cls.description,
        )
        assert hasattr(cls.stripe_customer, 'id') is True
        assert cls.stripe_customer.id is not None

    @classmethod
    def tearDownTestData(cls):
        stripe_res = stripe.Customer.delete(cls.stripe_customer.id)
        assert hasattr(stripe_res, 'deleted') is True
        assert stripe_res.get('deleted') is True

    def test_customer_exists(self):
        stripe_res = stripe.Customer.retrieve(self.stripe_customer.id)
        self.assertTrue(hasattr(stripe_res, 'email'))
        self.assertEqual(stripe_res.get('email'), self.email)
