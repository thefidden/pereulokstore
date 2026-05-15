from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class ProductReport(models.Model):
    """Модель отчета по товарам.

    Хранит сгенерированные PDF-отчеты о товарах с информацией
    о создателе и времени создания.

    Attributes:
        file: PDF-файл отчета.
        created_at: Дата и время создания отчета.
        created_by: Пользователь, создавший отчет.
    """
    file = models.FileField(upload_to = 'reports', verbose_name = 'PDF-отчет')
    created_at = models.DateTimeField(default = timezone.now, verbose_name = 'Дата создания')
    created_by = models.ForeignKey(
        User,
        on_delete = models.SET_NULL,
        null = True,
        blank = True,
        related_name = 'product_reports',
        verbose_name = 'Создано пользователем'
    )

    class Meta:
        verbose_name = 'Отчет по товарам'
        verbose_name_plural = 'Отчеты по товарам'
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f'Отчет от {self.created_at:%d-%m-%Y %H:%M}'
