from django.urls import path
from accounts.views import logout, login, registration, UserProfileView


urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', registration, name='registration'),
    path('profile/', UserProfileView.as_view(), name='profile'),
]
