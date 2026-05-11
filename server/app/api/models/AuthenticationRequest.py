from django.db import models
from api.models.AuthenticationToken import AuthenticationToken

class AuthenticationRequest(models.Model):
    """Модель запроса аутентификации через Telegram.

    Хранит данные пользователя Telegram для процесса аутентификации.

    Attributes:
        token: Связанный токен аутентификации (первичный ключ).
        telegram_id: ID пользователя в Telegram.
        telegram_username: Username пользователя в Telegram.
        telegram_name: Имя пользователя в Telegram.
        telegram_image: Аватар пользователя в бинарном формате.
    """
    token = models.OneToOneField(AuthenticationToken, primary_key = True, on_delete = models.CASCADE)

    telegram_id = models.BigIntegerField()
    telegram_username = models.CharField(max_length = 32, null = True)
    telegram_name = models.CharField(max_length = 128, null = True)
    telegram_image = models.BinaryField(null = True, editable = True)

    def __str__(self) -> str:
        return f'Telegram User [id: {self.telegram_id}, username: {self.telegram_username}, name: {self.telegram_name}]'
