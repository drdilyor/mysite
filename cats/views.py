from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from cats.models import Cat, Breed


class CatView(LoginRequiredMixin, ListView):
    model = Cat

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['breed_count'] = Breed.objects.all().count()
        return context


class CatCreate(LoginRequiredMixin, CreateView):
    model = Cat
    fields = '__all__'
    success_url = reverse_lazy('cats:cat_list')


class CatUpdate(LoginRequiredMixin, UpdateView):
    model = Cat
    fields = '__all__'
    success_url = reverse_lazy('cats:cat_list')


class CatDelete(LoginRequiredMixin, DeleteView):
    model = Cat
    success_url = reverse_lazy('cats:cat_list')


class BreedView(LoginRequiredMixin, ListView):
    model = Breed


class BreedCreate(LoginRequiredMixin, CreateView):
    model = Breed
    fields = '__all__'
    success_url = reverse_lazy('cats:breed_list')


class BreedUpdate(LoginRequiredMixin, UpdateView):
    model = Breed
    fields = '__all__'
    success_url = reverse_lazy('cats:breed_list')


class BreedDelete(LoginRequiredMixin, DeleteView):
    model = Breed
    success_url = reverse_lazy('cats:breed_list')
