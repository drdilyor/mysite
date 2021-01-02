from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import View

from ads.forms import AdForm
from ads.models import Ad
from ads.owner import OwnerListView, OwnerDetailView, OwnerDeleteView


class AdListView(OwnerListView):
    model = Ad


class AdDetailView(OwnerDetailView):
    model = Ad


class AdCreateView(LoginRequiredMixin, View):
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ads:index')
    
    def get(self, request, pk: int = None):
        form = AdForm()
        context = {'form': form}
        return render(request, self.template_name, context)
    
    def post(self, request, pk: int = None):
        form = AdForm(request.POST, request.FILES or None)

        if not form.is_valid():
            context = {'form': form}
            return render(request, self.template_name, context)

        # Add owner to the model before saving
        ad = form.save(commit=False)
        ad.owner = request.user
        ad.save()
        return redirect(self.success_url)


class AdUpdateView(LoginRequiredMixin, View):
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ads:index')

    def get(self, request, pk: int):
        ad = get_object_or_404(Ad, pk=pk, owner=request.user)
        form = AdForm(instance=ad)
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, pk: int):
        ad = get_object_or_404(Ad, pk=pk, owner=request.user)
        form = AdForm(request.POST, request.FILES or None, instance=ad)
        
        if not form.is_valid():
            context = {'form': form}
            return render(request, self.template_name, context)

        form.save()
        return render(self.success_url)


class AdDeleteView(OwnerDeleteView):
    model = Ad
    success_url = reverse_lazy('ads:index')

