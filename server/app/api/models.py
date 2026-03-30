import uuid

from django.contrib.auth.models import User
from django.contrib.postgres.indexes import GinIndex
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone

from .utils import get_product_image_path, get_user_image_path


class Product(models.Model):
    PRODUCT_TYPES = (
        # Сначала название в БД, затем название для внешнего отображения
        ('suit', 'Suit'),
        ('shape', 'Shape'),
        ('comics', 'Comics')
    )

    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False, unique = True)

    type = models.CharField(choices = PRODUCT_TYPES, max_length = 20)
    name = models.CharField(max_length = 50, editable = True)
    price = models.IntegerField(editable = True, validators = [MinValueValidator(0), MaxValueValidator(100_000)])
    description = models.CharField(editable = True, max_length = 1000)

    class Meta:
        indexes = [
            GinIndex(fields = ['name'], name = 'name_trgm', opclasses = ['gin_trgm_ops'])
        ]

    def __str__(self) -> str:
        return f'{self.name}'


class ProductImage(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False, unique = True)

    product = models.ForeignKey(Product, related_name = 'images', on_delete = models.CASCADE)
    image = models.ImageField(upload_to = get_product_image_path, null = True, default = None)

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


class Cart(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False, unique = True)

    user = models.ForeignKey(User, on_delete = models.PROTECT, related_name = 'cart')
    product = models.ForeignKey(Product, on_delete = models.PROTECT)
    amount = models.IntegerField(default = 1)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ['user', 'product'],
                name = 'unique_user_product'
            )
        ]

    def __str__(self) -> str:
        return f"Product {self.product.id} in user {self.user}'s cart"


class Order(models.Model):
    # Сначала название в БД, затем название для внешнего отображения
    STATUS_TYPES = (
        ('pending_payment', 'Pending Payment'),
        ('pending_assembly', 'Pending Assembly'),
        ('pending_pickup', 'Pending Pickup'),
        ('finished', 'Finished'),
        ('cancelled', 'Cancelled')
    )

    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False, unique = True)

    user = models.ForeignKey(User, on_delete = models.PROTECT, related_name = 'orders')
    price = models.IntegerField(default = 0, validators = [MinValueValidator(0)])
    status = models.CharField(choices = STATUS_TYPES, default = 'pending_payment', max_length = 20)
    datetime = models.DateTimeField(default = timezone.now)

    def __str__(self) -> str:
        return f'Заказ пользователя {self.user.username}'


class OrderProduct(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False, unique = True)

    order = models.ForeignKey(Order, related_name = 'products', on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.PROTECT)
    price = models.IntegerField(default = 0, validators = [MinValueValidator(0), MaxValueValidator(100_000)])
    amount = models.IntegerField(validators = [MinValueValidator(1), MaxValueValidator(10)])


class UserImage(models.Model):
    user = models.OneToOneField(User, related_name = 'image', primary_key = True, on_delete = models.CASCADE)
    image = models.ImageField(upload_to = get_user_image_path, null = True, default = None)

    def save(self, *args, **kwargs) -> None:
        try:
            old = UserImage.objects.get(user = self.user)
            if old.image != self.image:
                old.image.delete(save = False)
        except UserImage.DoesNotExist:
            pass

        super().save(*args, **kwargs)
