"""
The module contains TgTokenDaemon class which periodically fetches
bot updates and activates tokens
"""
import json
import re
from typing import Dict, Any

from django.urls import reverse
from telegram import Update, User
from telegram.ext import CommandHandler, CallbackContext, Updater


class TgTokenDaemon:
    # _instance = None
    #
    # @classmethod
    # def instance(cls):
    #     if cls._instance is None:
    #         cls._instance = cls()
    #     return cls._instance

    def __init__(self):
        from django.conf import settings

        print('==== CREATED DAEMON')
        u = Updater(settings.BOT_TOKEN, use_context=True)
        d = u.dispatcher
        d.add_handler(CommandHandler(['token', 'start'], self.handle_token))
        # start polling in development server
        if settings.DEBUG:
            u.bot.delete_webhook()
            u.start_polling()
        else:
            host = 'https://drdilyor.pythonanywhere.com'
            u.bot.set_webhook(host + reverse('users:webhook'))
        self._u = u

    def handle_token(self, update: Update, context: CallbackContext) -> bool:
        from .models import TgToken
        print('token handle')

        args = context.args

        if len(args) == 0:
            update.message.reply_text("Hi! This bot is used for drdilyor."
                                      "pythonanywhere.com login.")
            return False

        token = args[0]
        if not validate_token(token):
            update.message.reply_text("Invalid token.")
            return False

        u: User = update.message.from_user
        user = {
            'telegram_id': u.id,
            'first_name': u.first_name,
            'last_name': u.last_name,
            'username': u.username,
        }
        message = TgToken._token_activated(token, user)
        update.message.reply_text(message)
        update.message.reply_text(json.dumps(user, indent=4))
        return True

    def webhook_request(self, data: Dict[str, Any]):
        self._u.dispatcher.process_update(Update.de_json(data, self._u.bot))


    def stop(self) -> None:
        self._u.stop()

    def __del__(self):
        print('DELETED DAEMON===')
        self.stop()


def validate_token(token):
    """Checks if token is valid: only base64 chars are allowed"""
    return re.match(r'^[-a-zA-Z0-9_]+$', token) is not None
