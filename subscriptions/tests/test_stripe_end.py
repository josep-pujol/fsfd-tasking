import os

from django.contrib.auth.models import User
from django.shortcuts import reverseg
from django.test import TestCase
from subscriptions.views import PLAN_ID

import stripe
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')


class StripeApiTest(TestCase):
    @classmethod
    def setUp(self):
        # Create new Django user
        user2test = User.objects.create_user(
            username='user2test', email='usertest@email.com',
            password='XISRUkwtuK',
        )
        user2test.save()
        self.user2test = user2test

        # Create new Stripe Customer
        self.email = "user2test_stripe@gmail.com"
        self.description = "customer for user2test_stripe"
        self.stripe_customer = stripe.Customer.create(
            email=self.email,
            description=self.description,
        )
        assert hasattr(self.stripe_customer, 'id') is True
        assert self.stripe_customer.id is not None

        # # Create a subscription
        # self.stripe_subs = stripe.Subscription.create(
        #     customer=self.stripe_customer.id,
        #     items=[{'plan': PLAN_ID}, ]
        # )
        # assert hasattr(self.stripe_subs, 'id') is True
        # assert self.stripe_subs.id is not None

    @classmethod
    def tearDown(self):
        print('\nCUSTOMER teardown', self.stripe_customer.id)
        stripe_res = stripe.Customer.delete(self.stripe_customer.id)
        print('DELETE STRIPE CUSTOMER RES', stripe_res)
        assert hasattr(stripe_res, 'deleted') is True
        assert stripe_res.get('deleted') is True

    def test_customer_exists(self):
        print('\nCUSTOMER test_query_customer', self.stripe_customer.id)
        stripe_res = stripe.Customer.retrieve(self.stripe_customer.id)
        self.assertTrue(hasattr(stripe_res, 'email'))
        self.assertEqual(stripe_res.get('email'), self.email)

    # def test_payment(self):
    #     def createToken():
    #         token = stripe.Token.create(
    #             card={
    #                 "number": '4242424242424242',
    #                 "exp_month": 12,
    #                 "exp_year": 2022,
    #                 "cvc": '222'
    #             },
    #         )
    #         return token["id"]

    #     token = createToken()
    #     print('\nTOKEN', token)
    #     context = {
    #         'stripeEmail': [self.user2test.email, ],
    #         'stripeToken': [token, ],
    #         'stripeTokenType': ['card', ],
    #     }
    #     print('\nCONTEXT', context, '\n')
    #     # response = self.client.post(reverse('subscribe'), context)
    #     print('\nRESPONSE', response)

    # def test_payments(self):
    #     # Login user
    #     login = self.client.login(username='user2test', password='XISRUkwtuK')
    #     self.assertTrue(login)

    #     response = self.client.get('/subscriptions/')
    #     self.assertEqual(response.status_code, 200)
    #     print('\nRESPONSE GET', vars(response))

    #     print('\nRESPONSE context', response.context, '\n\n\n')
    #     for elem in response.context:
    #         print(vars(elem), '\n\nNEXT:\n')
            
    #     context = {
    #         'user': self.user2test,
    #         'POST': {'stripeToken': response.POST('stripeToken'), },
    #     }
    #     print('\nresponse', vars(response))
    #     print('\nCONTEXT', context, '\n')

    #     response = self.client.post(reverse('subscribe'), response)
    #     print('\nRESPONSE POST', response)