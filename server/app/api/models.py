import uuid

from django.contrib.auth.models import User
from django.contrib.postgres.indexes import GinIndex
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.db.models import Avg, Count, Max, Min, F

from .utils import get_product_image_path, get_user_image_path, get_report_file_path


class ProductQuerySet(models.QuerySet):
    def all(self):
        return (
            self
            .exclude(price__lt = 0)
            .exclude(creation_date__gt = timezone.now())
            .order_by('type', 'name')
        )

    def filter_name_contains(self, name: str):
        return self.filter(name__contains = name)

    def summary_values(self):
        return self.values('id', 'name', 'type', 'price', 'source_url')

    def summary_values_list(self):
        return self.values_list('id', 'name', 'source_url')

    def update_source_url(self, product_id, source_url: str):
        return self.filter(id = product_id).update(source_url = source_url)

    def with_images_count(self):
        return self.annotate(images_count = Count('images', distinct = True))

    def optimized(self):
        return self.prefetch_related('images', 'tags')


class ProductManager(models.Manager.from_queryset(ProductQuerySet)):
    def stats(self):
        return self.aggregate(
            avg_price = Avg('price'),
            min_price = Min('price'),
            max_price = Max('price'),
            total_products = Count('id')
        )


class Product(models.Model):
    PRODUCT_TYPES = (
        ('suit', 'Костюм'),
        ('shape', 'Фигурка'),
        ('comics', 'Комиксы')
    )

    objects = ProductManager()

    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False, unique = True)
    type = models.CharField(choices = PRODUCT_TYPES, max_length = 20, verbose_name = 'Категория')
    name = models.CharField(max_length = 50, editable = True, verbose_name = 'Название')
    slug = models.SlugField(max_length = 50, unique = True, null = True, blank = True, verbose_name = 'Slug')
    price = models.IntegerField(editable = True, validators = [MinValueValidator(0), MaxValueValidator(100_000)],
                                verbose_name = 'Цена')
    description = models.CharField(editable = True, max_length = 1000, verbose_name = 'Описание')
    source_url = models.URLField(null = True, blank = True, verbose_name = 'Ссылка на источник')
    creation_date = models.DateTimeField(default = timezone.now, verbose_name = 'Дата создания')
    tags = models.ManyToManyField('Tag', through = 'ProductTag', related_name = 'products', verbose_name = 'Теги')
    remaining = models.IntegerField(null = False, default = 10_000, validators = [MinValueValidator(0)],
                                    verbose_name = 'В наличии')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['name', 'creation_date']
        indexes = [
            GinIndex(fields = ['name'], name = 'name_trgm', opclasses = ['gin_trgm_ops'])
        ]

    def __str__(self) -> str:
        return f'{self.name}'

    def save(self, *args, **kwargs):
        is_new = self._state.adding

        super().save(*args, **kwargs)

        if is_new:
            update_fields = []

            if not self.slug:
                self.slug = f'{self.id}'
                update_fields.append('slug')

            if not self.source_url:
                self.source_url = f'https://pereulokstore/products/{self.id}/'
                update_fields.append('source_url')

            if update_fields:
                super().save(update_fields = update_fields)

    def get_absolute_url(self):
        return reverse('product-detail', kwargs = {'pk': self.id})


class ProductImage(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False, unique = True)

    product = models.ForeignKey(Product, related_name = 'images', on_delete = models.CASCADE, verbose_name = 'Товар')
    image = models.ImageField(upload_to = get_product_image_path, null = True, default = None,
                              verbose_name = 'Изображение')

    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товаров'

    def __str__(self) -> str:
        return f'Image for {self.product.name}'


class AuthenticationToken(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, unique = True, editable = False)


class AuthenticationRequest(models.Model):
    token = models.OneToOneField(AuthenticationToken, primary_key = True, on_delete = models.CASCADE)

    telegram_id = models.BigIntegerField()
    telegram_username = models.CharField(max_length = 32, null = True)
    telegram_name = models.CharField(max_length = 128, null = True)
    telegram_image = models.BinaryField(null = True, editable = True)

    def __str__(self) -> str:
        return f'Telegram User [id: {self.telegram_id}, username: {self.telegram_username}, name: {self.telegram_name}]'


class CartQuerySet(models.QuerySet):
    def user_items(self, user: User):
        return self.filter(user = user)

    def include_total_price(self):
        return self.annotate(total_price = F('amount') * F('product__price'))

    def optimized(self):
        return self.select_related('user', 'product')


class CartManager(models.Manager.from_queryset(CartQuerySet)):
    pass


class Cart(models.Model):
    objects = CartManager()

    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False, unique = True)
    user = models.ForeignKey(User, on_delete = models.PROTECT, related_name = 'cart', verbose_name = 'Пользователь')
    product = models.ForeignKey(Product, on_delete = models.PROTECT, verbose_name = 'Товар')
    amount = models.IntegerField(default = 1, verbose_name = 'Количество')
    creation_date = models.DateTimeField(default = timezone.now, verbose_name = 'Дата добавления')

    class Meta:
        verbose_name = 'Товары в корзине пользователей'
        verbose_name_plural = 'Товары в корзине пользователей'
        ordering = ['user__username', 'product__name']

        constraints = [
            models.UniqueConstraint(
                fields = ['user', 'product'],
                name = 'unique_user_product'
            )
        ]

    def __str__(self) -> str:
        return f"Product {self.product.id} in user {self.user}'s cart"


class OrderQuerySet(models.QuerySet):
    def user_orders(self, user: User):
        return self.filter(user = user)

    def optimized(self):
        return self.select_related('user').prefetch_related(
            'products__product__images',
            'products__product__tags'
        )


class OrderManager(models.Manager.from_queryset(OrderQuerySet)):
    pass


class Order(models.Model):
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
        """Возвращает товары на склад при отмене заказа."""
        for order_product in self.products.all():
            # Атомарное увеличение остатка
            order_product.product.remaining = F('remaining') + order_product.amount
            order_product.product.save(update_fields = ['remaining'])
            order_product.product.refresh_from_db()


class OrderProduct(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False, unique = True)

    order = models.ForeignKey(Order, related_name = 'products', on_delete = models.CASCADE, verbose_name = 'Заказ')
    product = models.ForeignKey(Product, on_delete = models.PROTECT, verbose_name = 'Товар')
    price = models.IntegerField(default = 0, validators = [MinValueValidator(0), MaxValueValidator(100_000)],
                                verbose_name = 'Цена')
    amount = models.IntegerField(validators = [MinValueValidator(1), MaxValueValidator(10)],
                                 verbose_name = 'Количество')

    class Meta:
        verbose_name = 'Товар заказа'
        verbose_name_plural = 'Товары заказов'


class UserImage(models.Model):
    user = models.OneToOneField(User, related_name = 'image', primary_key = True, on_delete = models.CASCADE,
                                verbose_name = 'Пользователь')
    image = models.ImageField(upload_to = get_user_image_path, null = True, default = None,
                              verbose_name = 'Изображение')

    def save(self, *args, **kwargs) -> None:
        try:
            old = UserImage.objects.get(user = self.user)
            if old.image != self.image:
                old.image.delete(save = False)
        except UserImage.DoesNotExist:
            pass

        super().save(*args, **kwargs)


class Tag(models.Model):
    """Теги для товаров (например: новинка, скидка, популярное)"""
    name = models.CharField(max_length = 50, unique = True, verbose_name = 'Название')
    slug = models.SlugField(max_length = 50, unique = True, blank = True, verbose_name = 'Slug')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['name']

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            import uuid
            # Генерируем slug из имени + уникальный суффикс для кириллицы
            base_slug = slugify(self.name) or f'tag-{uuid.uuid4().hex[:8]}'
            self.slug = base_slug

        super().save(*args, **kwargs)


class ProductTag(models.Model):
    """Промежуточная модель для связи Product и Tag с дополнительными полями"""
    product = models.ForeignKey(Product, on_delete = models.CASCADE, verbose_name = 'Товар')
    tag = models.ForeignKey(Tag, on_delete = models.CASCADE, verbose_name = 'Тег')
    added_at = models.DateTimeField(auto_now_add = True, verbose_name = 'Дата добавления')
    priority = models.IntegerField(default = 0, verbose_name = 'Приоритет отображения')

    class Meta:
        verbose_name = 'Тег товара'
        verbose_name_plural = 'Теги товаров'
        unique_together = [['product', 'tag']]
        ordering = ['-priority', '-added_at']

    def __str__(self) -> str:
        return f'{self.product.name} - {self.tag.name}'


class ProductReport(models.Model):
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
