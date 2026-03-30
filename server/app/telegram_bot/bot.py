import logging

import requests
from django.conf import settings
from requests import Response
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message
import telebot

from api.utils import get_user_image

bot = AsyncTeleBot(settings.TELEGRAM_BOT_TOKEN)
telebot.logger.setLevel(logging.CRITICAL)


@bot.message_handler(commands = ['start'])
async def start(message: Message):
    request_data: dict[str, str] = {
        'token': message.text.split(' ')[1],
        'telegram_id': message.chat.id,
        'telegram_name': message.from_user.full_name,
        'telegram_username': message.from_user.username
    }
    request_files: dict[str, bytes] = {
        'telegram_image': await get_user_image(bot = bot, user_id = message.chat.id)
    }

    response: Response = requests.post(
        url = f'http://127.0.0.1:8000/api/request-authentication/',
        data = request_data,
        files = request_files
    )

    if response.status_code == 201:
        return await bot.send_message(chat_id = message.chat.id, parse_mode = 'MarkdownV2', text = f'''
            Authenticating user```{'\n'.join([f'\t{key}: {request_data[key]}' for key in request_data])}```
        ''')
    else:
        return await bot.send_message(chat_id = message.chat.id, parse_mode = 'MarkdownV2', text = f'''
            Error authenticating user```{'\n'.join([f'\t{key}: {request_data[key]}' for key in request_data])}```
        ''')
