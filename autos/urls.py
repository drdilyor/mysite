from django.urls import path
from .views import *


app_name = 'autos'
urlpatterns = [
    path('', MainView.as_view(), name='all'),
    path('main/create/', AutoCreate.as_view(), name='auto_create'),
    path('main/<int:pk>/update/', AutoUpdate.as_view(), name='auto_update'),
    path('main/<int:pk>/delete/', AutoDelete.as_view(), name='auto_delete'),
    path('lookup/', MakeView.as_view(), name='make_list'),
    path('lookup/create/', MakeCreate.as_view(), name='make_create'),
    path('lookup/<int:pk>/update/', MakeUpdate.as_view(), name='make_update'),
    path('lookup/<int:pk>/delete/', MakeDelete.as_view(), name='make_delete'),
]
