from django.urls import path
from accounts.views import (logout, login, registration, UserProfileView,
                            UserUpdate)
from django.contrib.auth.decorators import login_required


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
]
