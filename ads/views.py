from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import View

from ads.forms import AdForm, CommentForm
from ads.models import Ad, Comment
from ads.owner import OwnerListView, OwnerDetailView, OwnerDeleteView


class AdListView(OwnerListView):
    model = Ad


class AdDetailView(OwnerDetailView):
    model = Ad


class AdDetailView(View):
    template_name = 'ads/ad_detail.html'

    def get(self, request, pk: int):
        ad = Ad.objects.get(pk=pk)
        comments = Comment.objects.filter(ad=ad).order_by('-created_at')
        form = CommentForm()
        context = {
            'ad': ad,
            'comments': comments,
            'comment_form': form,
        }
        return render(request, self.template_name, context)


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
        return redirect(self.success_url)


class AdDeleteView(OwnerDeleteView):
    model = Ad
    success_url = reverse_lazy('ads:index')


def stream_picture(request, pk: int):
    ad = get_object_or_404(Ad, pk=pk)

    if not ad.content_type:
        raise Http404

    response = HttpResponse()
    response['Content-Type'] = ad.content_type
    response['Content-Length'] = len(ad.picture)
    response.write(ad.picture)
    return response


@login_required
def create_comment(request, pk: int):
    if request.method == 'get':
        return redirect('ads:detail', pk=pk)

    ad = get_object_or_404(Ad, pk=pk)
    text = request.POST.get('comment')
    if not text or not (3 <= len(text) <= 500):
        return redirect('ads:detail', pk=pk)

    comment = Comment(text=text, ad=ad, owner=request.user)
    comment.save()
    return redirect('ads:detail', pk=pk)


class CommentDeleteView(OwnerDeleteView):
    model = Comment

    def get_success_url(self):
        ad = self.object.ad_id
        return reverse('ads:detail', kwargs={'pk': ad})
