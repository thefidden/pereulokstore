# Django Best Practices

Скилл основан на анализе реального проекта `server/app` — Django 6 + DRF + PostgreSQL + Telegram Bot + Alfa Bank.

---

## 1. Безопасность (Security)

### Секреты — только через переменные окружения
**Проблема в проекте**: `SECRET_KEY`, `TELEGRAM_BOT_TOKEN`, `ALFA_BANK_TOKEN`, пароль БД — всё хардкодом в `settings.py`.

```python
# ❌ Плохо (как сейчас)
SECRET_KEY = 'django-insecure-pb97u7k^...'
TELEGRAM_BOT_TOKEN = '8431694882:AAHS...'
DATABASES = {'default': {'PASSWORD': 'postgres'}}

# ✅ Хорошо
import os
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
DATABASES = {
    'default': {
        'PASSWORD': os.environ['DB_PASSWORD'],
    }
}
```

Использовать `python-dotenv` или `django-environ`. Файл `.env` добавить в `.gitignore`.

### DEBUG = False в продакшене
```python
# settings.py
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
```

### Разделять settings на dev/prod
```
app/settings/
    __init__.py
    base.py      # общие настройки
    dev.py       # DEBUG=True, SQLite
    prod.py      # DEBUG=False, PostgreSQL, HTTPS
```

---

## 2. Модели (Models)

### Кастомные QuerySet и Manager — правильный паттерн
В проекте используется хороший паттерн `Manager.from_queryset(QuerySet)`. Продолжать так же:

```python
class ProductQuerySet(models.QuerySet):
    def available(self):
        return self.filter(price__gte=0, creation_date__lte=timezone.now())

    def with_images_count(self):
        return self.annotate(images_count=Count('images', distinct=True))

class ProductManager(models.Manager.from_queryset(ProductQuerySet)):
    def stats(self):
        return self.aggregate(avg_price=Avg('price'), total=Count('id'))

class Product(models.Model):
    objects = ProductManager()
```

### Переопределение `all()` в QuerySet — осторожно
**Проблема**: `ProductQuerySet.all()` переопределён и фильтрует данные. Это ломает ожидаемое поведение Django (например, в admin).

```python
# ❌ Плохо — переопределять all()
def all(self):
    return self.exclude(price__lt=0)

# ✅ Хорошо — именованный метод
def available(self):
    return self.exclude(price__lt=0).exclude(creation_date__gt=timezone.now())
```

### Всегда указывать `related_name`
```python
# ✅ Как в проекте — хорошо
user = models.ForeignKey(User, related_name='cart', on_delete=models.PROTECT)
order = models.ForeignKey(Order, related_name='products', on_delete=models.CASCADE)
```

### `on_delete` — выбирать осознанно
- `CASCADE` — удалить связанные (изображения товара, позиции заказа)
- `PROTECT` — запретить удаление если есть связи (товар в корзине/заказе)
- `SET_NULL` — обнулить ссылку (опционально связанные данные)

### UUID как primary key — хорошая практика
```python
# ✅ Как в проекте
id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
```

### Meta класс — всегда заполнять
```python
class Meta:
    verbose_name = 'Заказ'
    verbose_name_plural = 'Заказы'
    ordering = ['-datetime']
    indexes = [models.Index(fields=['status', 'user'])]
    constraints = [
        models.UniqueConstraint(fields=['user', 'product'], name='unique_user_product')
    ]
```

---

## 3. Views и ViewSet

### Использовать `ModelViewSet` вместо ручного `ViewSet`
**Проблема**: В проекте все ViewSet написаны вручную с `@action` декораторами, хотя большинство — стандартные CRUD.

```python
# ❌ Как сейчас — много бойлерплейта
class Products(viewsets.ViewSet):
    @action(methods=['get'], detail=False)
    def list(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

# ✅ Лучше для стандартных CRUD
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['type']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'creation_date']

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsAdminUser()]
        return [AllowAny()]
```

### Проверка владельца — через permissions, не в теле view
**Проблема**: Проверки `if user != order.user: return 403` разбросаны по views.

```python
# ✅ Выделить в permission class
class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwner]
```

### Не дублировать `is_valid()` дважды
**Проблема в проекте** (`views.py`, Orders.create):
```python
# ❌ Плохо
if not order_serializer.is_valid():
    print(order_serializer.errors)
order_serializer.is_valid(raise_exception=True)  # вызов второй раз

# ✅ Хорошо
order_serializer.is_valid(raise_exception=True)
```

### Убрать `pprint` из продакшен кода
**Проблема**: `pprint.pprint(validated_data)` в `OrderSerializer.create()` и `views.py`.

---

## 4. Сериализаторы (Serializers)

### Вложенные сериализаторы — только для чтения
```python
# ✅ Как в проекте — хороший паттерн
class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)          # для чтения
    product_id = serializers.PrimaryKeyRelatedField(     # для записи
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )
```

### `SerializerMethodField` — для вычисляемых полей
```python
class ProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    
    def get_images(self, obj):
        request = self.context.get('request')
        return [request.build_absolute_uri(img.image.url) for img in obj.images.all()]
```

### Передавать `request` в контекст сериализатора
```python
# В view
serializer = ProductSerializer(product, context={'request': request})
```

### `select_related` / `prefetch_related` в QuerySet сериализатора
**Проблема**: `UserSerializer` включает `cart` и `orders` — это N+1 запросы.

```python
# ✅ В ViewSet
def get_queryset(self):
    return User.objects.prefetch_related(
        'cart__product__images',
        'orders__products__product'
    )
```

---

## 5. URL маршруты

### Использовать `DefaultRouter` для ViewSet
```python
# ✅ Вместо ручного path() для каждого метода
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('products', ProductViewSet, basename='product')
router.register('carts', CartViewSet, basename='cart')
router.register('orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
    # нестандартные маршруты добавлять отдельно
]
```

### Не использовать `from .views import *`
**Проблема в проекте** (`urls.py`): `from .views import *` — засоряет namespace.

```python
# ✅ Явный импорт
from .views import ProductViewSet, CartViewSet, OrderViewSet
```

---

## 6. Внешние HTTP-запросы (utils.py)

### Синхронные `requests` в async-контексте — проблема
**Проблема**: `utils.py` использует синхронный `requests` внутри async Telegram бота.

```python
# ❌ Плохо — блокирует event loop
import requests
file = requests.get(file_url).content

# ✅ Хорошо — использовать aiohttp (уже есть в зависимостях)
import aiohttp
async def get_user_image(bot, user_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(file_url) as resp:
            return await resp.read()
```

### Обработка ошибок внешних API
```python
# ✅ Всегда обрабатывать ошибки сети и API
def register_order(order):
    try:
        response = requests.post(url, data=data, timeout=10)
        response.raise_for_status()
        data = response.json()
        if 'errorCode' in data:
            raise PaymentError(data.get('errorMessage'))
        return data.get('formUrl')
    except requests.RequestException as e:
        logger.error(f'Payment registration failed: {e}')
        raise
```

### Таймауты для всех HTTP-запросов
```python
# ✅ Всегда указывать timeout
requests.post(url, data=data, timeout=10)
```

---

## 7. Admin

### Оптимизация запросов в admin
```python
# ✅ list_select_related для ForeignKey полей
class CartAdmin(admin.ModelAdmin):
    list_select_related = ('user', 'product')
    
# ✅ prefetch_related для M2M и reverse FK
class OrderAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('products__product')
```

### `@admin.display` вместо устаревшего атрибута
```python
# ✅ Как в проекте — хорошо
@admin.display(description='Количество позиций')
def products_count(self, obj):
    return obj.products.count()
```

---

## 8. Логирование

### Настроить `LOGGING` в settings
**Проблема**: В проекте используется `print()` для отладки.

```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
        'file': {
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs/django.log',
        },
    },
    'loggers': {
        'django': {'handlers': ['console'], 'level': 'INFO'},
        'api': {'handlers': ['console', 'file'], 'level': 'DEBUG'},
    },
}

# В коде
import logging
logger = logging.getLogger(__name__)

logger.info(f'Order {order.id} created for user {user.id}')
logger.error(f'Payment failed: {error}')
```

---

## 9. Производительность

### `select_related` для ForeignKey, `prefetch_related` для M2M/reverse FK
```python
# ✅ Избегать N+1 запросов
products = Product.objects.prefetch_related('images').all()
cart_items = Cart.objects.select_related('product', 'user').filter(user=user)
orders = Order.objects.prefetch_related('products__product__images').filter(user=user)
```

### Пагинация для list endpoints
```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}
```

### Кэширование для тяжёлых запросов
```python
from django.core.cache import cache

def get_product_stats():
    stats = cache.get('product_stats')
    if not stats:
        stats = Product.objects.stats()
        cache.set('product_stats', stats, timeout=300)
    return stats
```

---

## 10. Тестирование

### Структура тестов
```
api/
    tests/
        __init__.py
        test_models.py
        test_views.py
        test_serializers.py
        factories.py      # factory_boy
```

### Использовать `APITestCase` из DRF
```python
from rest_framework.test import APITestCase, APIClient

class ProductAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_superuser('admin', password='pass')
    
    def test_list_products(self):
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, 200)
    
    def test_create_product_requires_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post('/api/products/', data={...})
        self.assertEqual(response.status_code, 201)
```

---

## 11. Специфика этого проекта

### Telegram авторизация — добавить expiry для токенов
```python
class AuthenticationToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=10)
```

### Очистка корзины после заказа — через сигнал
```python
# signals.py
from django.db.models.signals import post_save

@receiver(post_save, sender=Order)
def clear_cart_on_order(sender, instance, created, **kwargs):
    if created:
        Cart.objects.filter(user=instance.user).delete()
```

### Платёжный статус — через Celery задачу, не синхронно
```python
# tasks.py
from celery import shared_task

@shared_task
def check_payment_status(order_id, bank_order_id):
    order = Order.objects.get(id=order_id)
    status = get_order_status(bank_order_id)
    if status == 2:
        order.status = 'pending_assembly'
        order.save()
```

---

## Быстрая шпаргалка

| Что | Как |
|-----|-----|
| Секреты | `os.environ` + `.env` файл |
| Кастомная логика запросов | `QuerySet` методы, не в `View` |
| Проверка прав | `Permission` классы, не `if user != obj.user` |
| Внешние запросы | Всегда `timeout=`, обработка ошибок |
| Отладка | `logger.debug()`, не `print()` |
| N+1 запросы | `select_related` / `prefetch_related` |
| Стандартный CRUD | `ModelViewSet` + `DefaultRouter` |
| Async контекст | `aiohttp`, не синхронный `requests` |
