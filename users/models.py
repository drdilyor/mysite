from datetime import timedelta
from typing import Tuple

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class TgLogin(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    telegram_id = models.IntegerField(primary_key=True)

    def __str__(self):
        return str(self.telegram_id)


class TgToken(models.Model):
    # region Fields
    token = models.CharField(primary_key=True, max_length=32)
    telegram_id = models.IntegerField(default=0, null=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64, blank=True, null=True)
    username = models.CharField(max_length=32, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    # endregion

    _expires_in = timedelta(minutes=30)

    def __str__(self):
        return f'{self.token} {self.telegram_id}'

    @property
    def is_activated(self):
        return self.telegram_id != 0

    @property
    def is_expired(self):
        return False  # TODO: do something useful

    def get_login_or_create(self, commit=True, delete=True
                            ) -> Tuple[User, TgLogin, bool]:
        self.__check()
        try:
            tg_login = TgLogin.objects.get(telegram_id=self.telegram_id)
            user = tg_login.user
            created = False

        except TgLogin.DoesNotExist:
            user = User(first_name=self.first_name)
            if self.username:
                user.username = self.username
            if self.last_name:
                user.last_name = self.last_name
            tg_login = TgLogin(user=user, telegram_id=self.telegram_id)

            if commit:
                user.save()
                tg_login.save()

            created = True

        if delete:
            self.__class__.objects.get(token=self.token).delete()
        return user, tg_login, created

    def __check(self):
        """If token is expired or not activated, throws error."""
        assert self.is_activated, "Token is not activated."
        assert not self.is_expired, "Token is expired."

    @classmethod
    def _token_activated(cls, token: str, user: dict) -> str:
        """
        Called when a `token` gets activated by `user`.
        Warning: not to be called manually
        """
        try:
            tk = cls.objects.get(token=token)
            tk.telegram_id = user['telegram_id']
            tk.first_name = user['first_name']
            tk.last_name = user.get('last_name')
            tk.username = user.get('username')
            tk.save()
            return 'Successful login.'
        except cls.DoesNotExist:
            return 'Invalid token.'


class TokenError(ValueError):
    pass
