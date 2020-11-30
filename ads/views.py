from django.shortcuts import render
from django.urls import reverse_lazy

from ads.models import Ad
from ads.owner import OwnerListView, OwnerDetailView, OwnerCreateView, \
    OwnerUpdateView, OwnerDeleteView


class AdListView(OwnerListView):
    model = Ad


class AdDetailView(OwnerDetailView):
    model = Ad


class AdCreateView(OwnerCreateView):
    model = Ad
    fields = ['title', 'price', 'text']
    success_url = reverse_lazy('ads:index')


class AdUpdateView(OwnerUpdateView):
    model = Ad
    fields = ['title', 'price', 'text']
    success_url = reverse_lazy('ads:index')


class AdDeleteView(OwnerDeleteView):
    model = Ad
    success_url = reverse_lazy('ads:index')
