from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import View, ListView, CreateView, UpdateView, \
    DeleteView

from autos.forms import AutoForm
from autos.models import Make, Auto


class MainView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest):
        make_count = Make.objects.all().count()
        autos = Auto.objects.all()
        return render(request, 'autos/auto_list.html', context={
            'make_count': make_count,
            'auto_list': autos,
        })


class AutoCreate(View):
    template = 'autos/auto_form.html'
    success_url = 'autos:all'

    def get(self, request: HttpRequest):
        form = AutoForm()
        return render(request, self.template, {'form': form})

    def post(self, request: HttpRequest):
        form = AutoForm(request.POST)
        if not form.is_valid():
            return render(request, self.template, {'form': form})
        else:
            form.save()
            return redirect(self.success_url)


class AutoUpdate(View):
    template = 'autos/auto_form.html'
    success_url = 'autos:all'

    def get(self, request: HttpRequest, pk: int):
        auto = get_object_or_404(Auto, pk=pk)
        form = AutoForm(instance=auto)
        return render(request, self.template, {'form': form})

    def post(self, request: HttpRequest, pk: int):
        auto = get_object_or_404(Auto, pk=pk)
        form = AutoForm(request.POST, instance=auto)
        if not form.is_valid():
            return render(request, self.template, {'form': form})
        else:
            form.save()
            return redirect(self.success_url)


class AutoDelete(View):
    success_url = 'autos:all'

    def get(self, request: HttpRequest, pk: int):
        return render(request, 'autos/auto_confirm_delete.html', {
            'auto': get_object_or_404(Auto, pk=pk)
        })

    def post(self, request: HttpRequest, pk: int):
        get_object_or_404(Auto, pk=pk).delete()
        return redirect(self.success_url)


class MakeView(ListView):
    model = Make
    template_name = 'make_list.html'


class MakeCreate(CreateView):
    model = Make
    fields = '__all__'
    success_url = reverse_lazy('autos:make_list')


class MakeUpdate(UpdateView):
    model = Make
    fields = '__all__'
    success_url = reverse_lazy('autos:make_list')


class MakeDelete(DeleteView):
    model = Make
    fields = '__all__'
    success_url = reverse_lazy('autos:make_list')
