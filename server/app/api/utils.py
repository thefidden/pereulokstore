"""Утилиты для работы с файлами, Telegram API и платежной системой."""

import os

import requests
from django.conf import settings
from telebot.async_telebot import AsyncTeleBot
from telebot.types import UserProfilePhotos, File


def get_product_image_path(instance, filename):
    """Генерирует путь для сохранения изображения товара.
    
    Args:
        instance: Экземпляр модели ProductImage.
        filename: Имя загружаемого файла.
        
    Returns:
        str: Путь вида 'products/{product_id}/{image_id}.jpg'.
    """
    return os.path.join('products', f'{instance.product.id}', f'{instance.id}.jpg')


def get_report_file_path(instance):
    """Генерирует путь для сохранения PDF-отчета.
    
    Args:
        instance: Экземпляр модели ProductReport.
        
    Returns:
        str: Путь вида '{REPORTS_ROOT}/{report_id}'.
    """
    return os.path.join(settings.REPORTS_ROOT, f'{instance.id}')


def get_user_image_path(instance, filename):
    """Генерирует путь для сохранения аватара пользователя.
    
    Args:
        instance: Экземпляр модели UserImage.
        filename: Имя загружаемого файла.
        
    Returns:
        str: Путь вида 'users/{user_id}.jpg'.
    """
    return os.path.join('users', f'{instance.user.id}.jpg')


async def get_user_image(bot: AsyncTeleBot, user_id: int):
    """Получает аватар пользователя из Telegram.
    
    Args:
        bot: Экземпляр Telegram бота.
        user_id: ID пользователя в Telegram.
        
    Returns:
        bytes: Бинарные данные изображения или пустая строка.
    """
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
    """Регистрирует заказ в платежной системе Альфа-Банка.
    
    Args:
        order: Экземпляр модели Order для регистрации.
        
    Returns:
        str: URL формы оплаты или пустая строка при ошибке.
    """
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
    """Получает статус оплаты заказа из платежной системы.
    
    Возможные значения orderStatus:
        0 - заказ зарегистрирован, но не оплачен;
        1 - заказ только авторизован (для двухстадийных платежей);
        2 - заказ авторизован и завершен;
        3 - авторизация отменена;
        4 - по транзакции была проведена операция возврата;
        5 - инициирована авторизация через ACS банка-эмитента;
        6 - авторизация отклонена;
        7 - ожидание оплаты заказа;
        8 - промежуточное завершение для многократного частичного завершения.
    
    Args:
        bank_order_id: ID заказа в платежной системе.
        
    Returns:
        int: Код статуса заказа.
    """

    request = requests.post(url = 'https://alfa.rbsuat.com/payment/rest/getOrderStatusExtended.do', data = {
        'token': settings.ALFA_BANK_TOKEN,
        'orderId': bank_order_id
    })
    response = request.json()
    order_status: int = response.get('orderStatus')
    return order_status
