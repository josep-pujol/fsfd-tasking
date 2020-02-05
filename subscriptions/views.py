import os

from django.contrib import messages
from django.shortcuts import redirect, render, reverse
from django.contrib.auth.decorators import login_required

from subscriptions.models import PremiumUser
import stripe

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')


@login_required
def checkout(request):
    # try:
    #     if request.user.premiumuser:
    #         return redirect(reverse('index'))
    # except PremiumUser.DoesNotExist:
    #     pass
    # except AttributeError:
    #     pass

    plan_id = 'plan_Gcb3Ira0nEPtnk'
    if request.method == 'POST':
        stripe_customer = stripe.Customer.create(
            email=request.user.email, source=request.POST['stripeToken']
        )
        subscription = stripe.Subscription.create(
            customer=stripe_customer.id, items=[{'plan': plan_id}, ]
        )
        premiumuser = PremiumUser()
        premiumuser.user = request.user
        premiumuser.stripe_id = stripe_customer.id
        premiumuser.stripe_subscription_id = subscription.id
        premiumuser.save()
        messages.success(request, 'Payment processed succesfully')
        messages.success(
            request, 
            f'You are now a Premium user { request.user.username.title() }!')
        return redirect('index')
    else:
        price = 9900
        final_euro = 99
        return render(
            request,
            'subscriptions/checkout.html',
            {
                'stripe_public_key': os.getenv('STRIPE_PUBLIC_KEY'),
                'plan': plan_id, 'price': price, 'final_euro': final_euro,
            },
        )
