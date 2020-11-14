from django.conf import settings
from django.urls import path

from .views import *

app_name = 'users'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path(f'{settings.BOT_TOKEN}/', webhook, name='webhook'),
]