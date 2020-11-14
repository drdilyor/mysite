import json

from django.contrib.auth import login
from django.http import HttpRequest, HttpResponseRedirect, Http404, \
    HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

from users.models import TgToken


class LoginView(View):
    def get(self, request: HttpRequest, **kwargs):
        s = request.session  # noqa

        if not s.session_key:
            s.create()
            TgToken(token=s.session_key).save()

        return render(request, 'users/login.html', context={
            'link': self.get_link(),
            'next': request.GET.get('next'),
        })

    def post(self, request: HttpRequest, **kwargs):
        s = request.session  # noqa

        try:
            token: TgToken = TgToken.objects.get(token=s.session_key)  # noqa
            error_messages = []
            if not token.is_activated:
                error_messages.append('Token is not activated')
            if token.is_expired:
                error_messages.append('Token is expired')

            if not error_messages:
                user, tg_login, created = token.get_login_or_create(delete=False)
                login(request, user)
                url = request.POST.get('next', reverse('index'))
                return HttpResponseRedirect(url)
            else:
                return render(request, 'users/login.html', context={
                    'link': self.get_link(),
                    'next': request.POST.get('next'),
                })

        except TgToken.DoesNotExist:  # noqa
            # in case token is deleted but session is not
            if request.session.session_key:
                request.session.flush()

            return HttpResponseRedirect(reverse('users:login'))



    def get_link(self):
        from django.conf import settings
        token = self.request.session.session_key
        return f'http://t.me/{settings.BOT_USERNAME}/?start={token}'


@csrf_exempt
def webhook(request: HttpRequest):
    if request.method == 'POST':
        from django.apps import apps
        daemon = apps.get_app_config('users').daemon
        try:
            daemon.webhook_request(json.loads(request.body))
            return HttpResponse('ok')
        except ValueError:
            return HttpResponseBadRequest()
    else:
        raise Http404()