from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import path, reverse_lazy

from accounts.views import (logout, login, registration, UserProfileView,
                            UserUpdate)


urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', registration, name='registration'),
    path(
        'profile/',
        login_required(UserProfileView.as_view()),
        name='profile'
    ),
    path(
        'update-profile/<int:pk>/',
        login_required(UserUpdate.as_view()),
        name='update_profile'
    ),
    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='accounts/change_password.html',
            success_url=reverse_lazy('profile')
        ),
        name='change_password'
    ),
]
