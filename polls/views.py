from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic as g

from polls.models import Question, Vote, Choice


class IndexView(g.ListView):
    model = Question
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]  # noqa


class DetailView(g.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get(self, request, **kwargs):
        question = self.get_object()
        question.view_count += 1
        question.save()
        return super().get(request, **kwargs)


class VoteRequiredMixin:
    """Mixin checks if user has voted on a question.
    Assuming user is already authenticated
    """
    def dispatch(self, request: HttpRequest, **kwargs):
        question: Question = get_object_or_404(Question, pk=self.kwargs['pk'])
        self.user_choice = Vote.objects.get(
            user=request.user,
            question=question,
        ).choice
        if self.user_choice:
            return super().dispatch(request, **kwargs)
        else:
            return HttpResponseRedirect(question.get_absolute_url())

    def get_context_data(self, **kwargs):
        context = {}
        if self.user_choice:
            context['user_choice'] = self.user_choice
        context.update(kwargs)
        return super().get_context_data(**context)


class ResultsView(LoginRequiredMixin, VoteRequiredMixin, g.DetailView):
    model = Question
    template_name = 'polls/results.html'


def results(request: HttpRequest, question_id: int):
    try:
        user_choice = Vote.objects.get(  # noqa
            user_id=request.user.id,  # noqa
            question_id=question_id
        ).choice_id

    except Vote.DoesNotExist:  # noqa
        request.session['error'] = "You have not voted on the question"  # noqa
        return HttpResponseRedirect(
            reverse('polls:detail', args=(question_id,))
        )

    else:
        question = get_object_or_404(Question, pk=question_id)
        return render(request, 'polls/results.html', context={
            'question': question,
            'user_choice': user_choice,
        })


@login_required
def vote(request: HttpRequest, question_id: int):
    question = get_object_or_404(Question, pk=question_id)
    try:
        choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', context={
            'question': question,
            'error_message': "You didn't select a choice."
        })
    else:
        try:
            # user has already voted
            vote = Vote.objects.get(user=request.user, question=question)
            vote.choice = choice
        except Vote.DoesNotExist:
            # else create a vote
            vote = Vote(question=question, choice=choice, user=request.user)
        vote.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
