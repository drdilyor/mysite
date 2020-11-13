from typing import Optional

from django.apps import AppConfig

from .tgdaemon import TgTokenDaemon


class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        self.daemon = TgTokenDaemon()
