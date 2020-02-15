from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from tasks.models import Team, UserTeam

import stripe

from decimal import Decimal

import json
import time


class StripeUserTest(TestCase):
    @classmethod
    def setUp(self):
        # Create new Stripe Customer
        self.email = "user2test_stripe@gmail.com"
        self.description = "customer for user2test_stripe",
        self.stripe_customer = stripe.Customer.create(
            email=self.email,
            description=self.description,
        )
        print('\nCUSTOMER 1', self.stripe_customer)
        print(dir(self.stripe_customer), '\n\n', self.stripe_customer.id)
        self.assertIsNotNone(self.stripe_customer.id)

    @classmethod
    def tearDown(self):
        print('\nCUSTOMER 2', self.stripe_customer_id)
        stripe_res = stripe.Customer.delete(self.stripe_customer_id)
        print('DELETE STRIPE CUSTOMER RES', stripe_res)
        self.assertTrue(hasattr(stripe_res, 'deleted'))
        self.assertTrue(stripe_res.get('deleted'))

    def test_query_customer(self):
        print('\nCUSTOMER 3', self.stripe_customer_id)
        stripe_res = stripe.Customer.retrieve(self.stripe_customer_id)
        self.assertTrue(hasattr(stripe_res, 'email'))
        self.assertEqual(stripe_res.get('email'), self.email)

    def test_customer_can_be_charged(self):
        # with an account balance of $0 #yes the customer can be charged
        # as long there is a source(card or otherwise link to the account)
        self.assertEqual(
            self.customer.can_charge(), True, 'customer cant be charged')
