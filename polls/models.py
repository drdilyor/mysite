from django.contrib.auth import get_user_model
from django.db import models as m
from django.urls import reverse

User = get_user_model()


class Question(m.Model):
    title = m.CharField(max_length=200)
    description = m.TextField()
    author = m.ForeignKey(User, on_delete=m.CASCADE)
    pub_date = m.DateTimeField()
    view_count = m.IntegerField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('polls:detail', kwargs={'pk': self.id})


class Choice(m.Model):
    question = m.ForeignKey(Question, on_delete=m.CASCADE)
    choice_text = m.CharField(max_length=200)

    def __str__(self):
        return self.choice_text

    def get_vote_count(self):
        l = len(Vote.objects.filter(choice=self))
        print(l)
        return l


class Vote(m.Model):
    question = m.ForeignKey(Question, on_delete=m.CASCADE)
    choice = m.ForeignKey(Choice, on_delete=m.CASCADE)
    user = m.ForeignKey(User, on_delete=m.CASCADE)
