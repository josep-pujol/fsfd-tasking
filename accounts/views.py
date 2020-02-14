from django.shortcuts import redirect, render, reverse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import UpdateView

from accounts.forms import UserLoginForm, UserRegistrationForm
from tasks.models import Team, UserTeam


def index(request):
    """Return landing page"""
    if hasattr(request.user, 'team_owner'):
        return redirect(reverse('user_tasks'))
    elif request.user.is_authenticated:
        # User registered but not premium
        return redirect(reverse('subscribe'))
    else:
        # Unknown user
        return render(request, 'accounts/index.html')


@login_required
def logout(request):
    """Logout user"""
    auth.logout(request)
    messages.success(request, 'Logged out')
    messages.success(request, 'See you soon!')
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
                messages.success(request, f'Logged in')
                messages.success(
                    request, f'Welcome { user.username.title() }!')
                return redirect(reverse('index'))
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

                # Add user to default UserTeam
                default_team = Team.objects.get(pk=1)
                user_team = UserTeam.objects.create(
                    ut_user=user, ut_team=default_team)
                user_team.save()

                messages.success(request, 'You are registered!')
                messages.success(
                    request, f'Welcome to Tasking  { user.username.title() }!')
                return redirect(reverse('index'))
            else:
                messages.error(request, 'Unable to register at this time')
                messages.error(request, 'Please try again')
    else:
        registration_form = UserRegistrationForm()

    return render(
        request,
        'accounts/registration.html',
        {'registration_form': registration_form},
    )


class UserProfileView(View):
    template_name = 'accounts/profile.html'

    def get(self, request, *args, **kwargs):
        user_profile = request.user
        return render(
            request, self.template_name, {'user_profile': user_profile}, )


class UserUpdate(UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'username', 'email', ]
    template_name = 'accounts/update_profile.html'
    success_url = reverse_lazy('profile')
    # def get(self, request, *args, **kwargs):
    #     print(self.template_name)
    #     user = request.user
    #     return render(
    #         request, self.template_name, {'form': form, 'user': user}, )

    # def post(self, request, *args, **kwargs):
    #     form = self.form_class(request.POST)
    #     if form.is_valid():
    #         print('# <process form cleaned data>')
    #         return redirect('/profile/')

    #     return render(request, self.template_name, {'form': form})
