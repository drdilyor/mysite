from django.urls import path
from .views import *


app_name = 'cats'
urlpatterns = [
    path('', CatView.as_view(), name='all'),
    path('', CatView.as_view(), name='cat_list'),
    path('main/create/', CatCreate.as_view(), name='cat_create'),
    path('main/<int:pk>/update/', CatUpdate.as_view(), name='cat_update'),
    path('main/<int:pk>/delete/', CatDelete.as_view(), name='cat_delete'),
    path('lookup/', BreedView.as_view(), name='breed_list'),
    path('lookup/create/', BreedCreate.as_view(), name='breed_create'),
    path('lookup/<int:pk>/update/', BreedUpdate.as_view(), name='breed_update'),
    path('lookup/<int:pk>/delete/', BreedDelete.as_view(), name='breed_delete'),
]
