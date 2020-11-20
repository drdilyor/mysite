from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from cats.models import Cat, Breed


class CatView(ListView):
    model = Cat

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['breed_count'] = Breed.objects.all().count()
        return context


class CatCreate(CreateView):
    model = Cat
    fields = '__all__'
    success_url = reverse_lazy('cats:cat_list')


class CatUpdate(UpdateView):
    model = Cat
    fields = '__all__'
    success_url = reverse_lazy('cats:cat_list')


class CatDelete(DeleteView):
    model = Cat
    success_url = reverse_lazy('cats:cat_list')


class BreedView(ListView):
    model = Breed


class BreedCreate(CreateView):
    model = Breed
    fields = '__all__'
    success_url = reverse_lazy('cats:breed_list')


class BreedUpdate(UpdateView):
    model = Breed
    fields = '__all__'
    success_url = reverse_lazy('cats:breed_list')


class BreedDelete(DeleteView):
    model = Breed
    success_url = reverse_lazy('cats:breed_list')
