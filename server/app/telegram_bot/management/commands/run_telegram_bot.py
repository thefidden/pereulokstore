import asyncio

from django.core.management import BaseCommand
from telegram_bot.bot import bot


class Command(BaseCommand):
    help = 'Run Telegram Bot'

    def handle(self, *args, **kwargs) -> None:
        self.stdout.write('Telegram Bot Running')
        asyncio.run(bot.infinity_polling())