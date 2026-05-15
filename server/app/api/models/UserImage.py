from django.contrib.auth.models import User
from django.db import models

from api.utils import get_user_image_path


class UserImage(models.Model):
    """Модель изображения профиля пользователя.

    Хранит аватар пользователя, загруженный из Telegram.
    При обновлении изображения старое автоматически удаляется.

    Attributes:
        user: Пользователь (первичный ключ, связь один-к-одному).
        image: Файл изображения профиля.
    """
    user = models.OneToOneField(User, related_name = 'image', primary_key = True, on_delete = models.CASCADE,
                                verbose_name = 'Пользователь')
    image = models.ImageField(upload_to = get_user_image_path, null = True, default = None,
                              verbose_name = 'Изображение')

    def save(self, *args, **kwargs) -> None:
        """Сохраняет изображение профиля, удаляя старое при обновлении.

        Args:
            *args: Позиционные аргументы для родительского метода save.
            **kwargs: Именованные аргументы для родительского метода save.
        """
        try:
            old = UserImage.objects.get(user = self.user)
            if old.image != self.image:
                old.image.delete(save = False)
        except UserImage.DoesNotExist:
            pass

        super().save(*args, **kwargs)
