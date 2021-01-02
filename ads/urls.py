from django.urls import path
from django.views.generic import RedirectView

from .views import *

app_name = 'ads'
urlpatterns = [
    path('ads/', AdListView.as_view(), name='index'),
    path('ad/create', AdCreateView.as_view(), name='create'),
    path('ad/<int:pk>/', AdDetailView.as_view(), name='detail'),
    path('ad/<int:pk>/update', AdUpdateView.as_view(), name='update'),
    path('ad/<int:pk>/delete', AdDeleteView.as_view(), name='delete'),
    path('ad_picture/<int:pk>', stream_picture, name='ad_picture'),
    path('ad/<int:pk>/comment', create_comment, name='comment_create'),
]
