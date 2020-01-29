from django.shortcuts import render, redirect, reverse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from accounts.forms import UserLoginForm, UserRegistrationForm


def index(request):
    """Return the index.html file"""
    return render(request, 'accounts/index.html')


def logout(request):
    """Logout user"""
    auth.logout(request)
    return redirect(reverse('index'))


def login(request):
    """Return Login Page"""
    if request.user.is_authenticated:
        return redirect(reverse('index'))
    if request.method == 'POST':
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(
                request=request,
                username=request.POST['username_or_email'],
                password=request.POST['password']
            )
            if user:
                auth.login(user=user, request=request)
                return redirect(reverse(('index')))
            else:
                login_form.add_error(None, 'Incorrect login details')
    else:
        login_form = UserLoginForm()

    return render(request, 'accounts/login.html', {'login_form': login_form})


def registration(request):
    """Render the registration page"""

    if request.user.is_authenticated:
        return redirect(reverse(('index')))

    if request.method == 'POST':
        registration_form = UserRegistrationForm(request.POST)
        if registration_form.is_valid():
            registration_form.save()
            user = auth.authenticate(
                request=request,
                username=request.POST['username'],
                password=request.POST['password1']
            )
            if user:
                auth.login(user=user, request=request)
                messages.success(request, 'You are registered')
                return redirect(reverse('index'))
            else:
                messages.error(request, 'Unable to register at this time')
    else:
        registration_form = UserRegistrationForm()

    return render(request, 'accounts/registration.html',
                  {'registration_form': registration_form})

# TODO
@login_required
def user_profile(request):
    """User's profile Page"""

    user = User.objects.get(email=request.user.email)
    return render(request, 'accounts/profile.html', {'profile': user})
