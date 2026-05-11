import uuid

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import F
from django.utils import timezone


class OrderQuerySet(models.QuerySet):
    """QuerySet для модели Order с методами фильтрации и оптимизации."""

    def user_orders(self, user: User):
        """Возвращает заказы конкретного пользователя."""
        return self.filter(user = user)

    def optimized(self):
        """Оптимизирует запрос с prefetch товаров, изображений и тегов."""
        return self.select_related('user').prefetch_related(
            'products__product__images',
            'products__product__tags'
        )


class OrderManager(models.Manager.from_queryset(OrderQuerySet)):
    pass


class Order(models.Model):
    """Модель заказа пользователя.

    Attributes:
        id: Уникальный идентификатор заказа (UUID).
        user: Пользователь, создавший заказ.
        price: Общая стоимость заказа.
        status: Текущий статус заказа.
        datetime: Дата и время создания заказа.
    """
    # Сначала название в БД, затем название для внешнего отображения
    STATUS_TYPES = (
        ('pending_payment', 'Ожидает оплаты'),
        ('pending_assembly', 'Собирается'),
        ('pending_pickup', 'Можно забирать'),
        ('finished', 'Завершен'),
        ('cancelled', 'Отменен')
    )

    objects = OrderManager()

    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False, unique = True)
    user = models.ForeignKey(User, on_delete = models.PROTECT, related_name = 'orders', verbose_name = 'Пользователь')
    price = models.IntegerField(default = 0, validators = [MinValueValidator(0)], verbose_name = 'Цена')
    status = models.CharField(choices = STATUS_TYPES, default = 'pending_payment', max_length = 20,
                              verbose_name = 'Статус')
    datetime = models.DateTimeField(default = timezone.now, verbose_name = 'Дата')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-datetime']

    def __str__(self) -> str:
        return f'Заказ пользователя {self.user.username}'

    def restore_stock(self):
        """Возвращает товары на склад при отмене заказа.

        Атомарно увеличивает остатки всех товаров в заказе на количество,
        указанное в OrderProduct. Использует F() выражения для безопасного
        обновления на уровне базы данных.
        """
        for order_product in self.products.all():
            # Атомарное увеличение остатка
            order_product.product.remaining = F('remaining') + order_product.amount
            order_product.product.save(update_fields = ['remaining'])
            order_product.product.refresh_from_db()
