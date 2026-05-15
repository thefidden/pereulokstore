import uuid

from django.db import models


class AuthenticationToken(models.Model):
    """Модель токена аутентификации.

    Используется для временного хранения токенов при аутентификации
    через Telegram.

    Attributes:
        id: Уникальный идентификатор токена (UUID).
    """
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, unique = True, editable = False)
