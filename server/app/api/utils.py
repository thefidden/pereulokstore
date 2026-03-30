import os
import requests
import pprint

from django.conf import settings
from telebot import TeleBot
from telebot.async_telebot import AsyncTeleBot
from telebot.types import UserProfilePhotos, File


def get_product_image_path(instance, filename):
    return os.path.join('products', f'{instance.product.id}', f'{instance.id}.jpg')


def get_user_image_path(instance, filename):
    return os.path.join('users', f'{instance.user.id}.jpg')


async def get_user_image(bot: AsyncTeleBot, user_id: int):
    photos: UserProfilePhotos = await bot.get_user_profile_photos(user_id)

    if not photos.total_count:
        return ''

    file_id = photos.photos[0][-1].file_id
    file_info: File = await bot.get_file(file_id)
    file_path = file_info.file_path

    file_url = f'https://api.telegram.org/file/bot{settings.TELEGRAM_BOT_TOKEN}/{file_path}'
    file = requests.get(file_url).content

    return file


def register_order(order: 'Order') -> str:
    request = requests.post(url = 'https://alfa.rbsuat.com/payment/rest/register.do', data = {
        'token': settings.ALFA_BANK_TOKEN,
        'orderNumber': order.id,
        'amount': order.price,
        'clientId': order.user.id,
        'returnUrl': f'https://pereulokstore.ru/orders/{order.id}/payment/check'
    })
    response = request.json()

    return response.get('formUrl')

def get_order_status(bank_order_id: str):
    # Значения параметра orderStatus (статус оплаты)
    # 0 - заказ зарегистрирован, но не оплачен;
    # 1 - заказ только авторизован и еще не завершен (для двухстадийных платежей);
    # 2 - заказ авторизован и завершен;
    # 3 - авторизация отменена;
    # 4 - по транзакции была проведена операция возврата;
    # 5 - инициирована авторизация через ACS банка-эмитента;
    # 6 - авторизация отклонена;
    # 7 - ожидание оплаты заказы;
    # 8 - промежуточное завершение для многократного частичного завершения.

    request = requests.post(url = 'https://alfa.rbsuat.com/payment/rest/getOrderStatusExtended.do', data = {
        'token': settings.ALFA_BANK_TOKEN,
        'orderId': bank_order_id
    })
    response = request.json()
    order_status: int = response.get('orderStatus')
    return order_status



