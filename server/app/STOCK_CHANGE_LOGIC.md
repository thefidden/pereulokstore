# Логика изменения количества товаров при создании заказа

**Дата:** 11 мая 2026  
**Версия:** 2.0

---

## Обзор

Реализована полная система управления остатками товаров с поддержкой:
- ✅ Уменьшение остатков при создании заказа
- ✅ Восстановление остатков при отмене заказа
- ✅ Восстановление остатков при неудачной оплате
- ✅ Атомарные операции с использованием транзакций
- ✅ Защита от race conditions с помощью блокировок

---

## Архитектура решения

### 1. Создание заказа (OrderViewSet.create)

```python
@transaction.atomic
def create(self, request: Request) -> Response:
    # 1. Проверка авторизации
    if not user.is_authenticated:
        return Response(status = 403)
    
    # 2. Получение товаров с блокировкой
    cart_items = (
        Cart.objects
        .user_items(user)
        .select_related('product')
        .select_for_update()  # Блокировка строк
    )
    
    # 3. Проверка остатков
    insufficient_stock = []
    for cart_item in cart_items:
        if cart_item.product.remaining < cart_item.amount:
            insufficient_stock.append({...})
    
    if insufficient_stock:
        return Response({'insufficient_stock': ...}, status = 400)
    
    # 4. Создание заказа
    order_serializer.save()
    
    # 5. Уменьшение остатков (атомарно)
    for cart_item in cart_items:
        cart_item.product.remaining = F('remaining') - cart_item.amount
        cart_item.product.save(update_fields = ['remaining'])
        cart_item.product.refresh_from_db()
    
    return Response({'order': ..., 'formUrl': ...}, status = 201)
```

**Ключевые особенности:**
- `@transaction.atomic` - вся операция выполняется в одной транзакции
- `select_for_update()` - блокирует строки до конца транзакции
- `F('remaining') - amount` - атомарное обновление на уровне БД

---

### 2. Восстановление остатков (Order.restore_stock)

```python
def restore_stock(self):
    """Возвращает товары на склад при отмене заказа."""
    from django.db.models import F
    for order_product in self.products.all():
        # Атомарное увеличение остатка
        order_product.product.remaining = F('remaining') + order_product.amount
        order_product.product.save(update_fields = ['remaining'])
        order_product.product.refresh_from_db()
```

**Расположение:** `api/models.py` - метод модели `Order`

---

### 3. Удаление заказа (OrderViewSet.delete)

```python
@transaction.atomic
def delete(self, request: Request, pk) -> Response:
    order = get_object_or_404(Order, pk = pk)
    
    # Проверка прав доступа
    if user != order.user:
        return Response(status = 403)
    
    # Возвращаем товары только для незавершенных заказов
    if order.status in ['pending_payment', 'pending_assembly']:
        order.restore_stock()
    
    order.delete()
    return Response(status = 204)
```

**Логика восстановления:**
- ✅ `pending_payment` - товары возвращаются
- ✅ `pending_assembly` - товары возвращаются
- ❌ `pending_pickup` - товары НЕ возвращаются
- ❌ `finished` - товары НЕ возвращаются
- ❌ `cancelled` - товары НЕ возвращаются

---

### 4. Проверка оплаты (OrderViewSet.check_payment_status)

```python
def check_payment_status(self, request: Request, pk) -> Response:
    order_status = get_order_status(bank_order_id)
    order = get_object_or_404(Order, pk = pk)
    
    if order_status == 2:
        # Оплата успешна
        order.status = 'pending_assembly'
        order.save()
        return Response({'paymentStatus': 'successful'}, status = 200)
    else:
        # Оплата не прошла - возвращаем товары
        order.restore_stock()
        order.delete()
        return Response({'paymentStatus': 'failure'}, status = 200)
```

---

## Жизненный цикл заказа

```
1. Создание заказа
   ├─ Проверка остатков
   ├─ Создание Order
   └─ Уменьшение остатков ✅
   
2. Ожидание оплаты (pending_payment)
   ├─ Оплата успешна → pending_assembly
   └─ Оплата не прошла → restore_stock() + delete ✅
   
3. Сборка заказа (pending_assembly)
   └─ Отмена → restore_stock() + delete ✅
   
4. Готов к выдаче (pending_pickup)
   └─ Отмена → delete (БЕЗ restore_stock)
   
5. Завершен (finished)
   └─ Удаление → delete (БЕЗ restore_stock)
```

---

## Защита от race conditions

### Проблема
Два пользователя одновременно заказывают последний товар:

```
Время | Пользователь A          | Пользователь B
------|-------------------------|-------------------------
T1    | Читает: remaining = 1   |
T2    |                         | Читает: remaining = 1
T3    | Проверка: 1 >= 1 ✅     |
T4    |                         | Проверка: 1 >= 1 ✅
T5    | Создает заказ           |
T6    |                         | Создает заказ
T7    | remaining = 0           |
T8    |                         | remaining = -1 ❌
```

### Решение: select_for_update()

```python
cart_items = Cart.objects.select_for_update().filter(user=user)
```

**Как работает:**

```
Время | Пользователь A          | Пользователь B
------|-------------------------|-------------------------
T1    | SELECT ... FOR UPDATE   |
T2    | Блокировка установлена  |
T3    |                         | SELECT ... FOR UPDATE
T4    |                         | Ожидает разблокировки...
T5    | Проверка: 1 >= 1 ✅     |
T6    | Создает заказ           |
T7    | remaining = 0           |
T8    | COMMIT (разблокировка)  |
T9    |                         | Блокировка получена
T10   |                         | Проверка: 0 >= 1 ❌
T11   |                         | Ошибка: недостаточно
```

---

## Атомарные операции с F()

### Проблема обычного подхода

```python
# ❌ НЕ атомарно
product.remaining = product.remaining - amount
product.save()
```

**Проблема:** Между чтением и записью значение может измениться.

### Решение: F() выражения

```python
# ✅ Атомарно
from django.db.models import F
product.remaining = F('remaining') - amount
product.save(update_fields = ['remaining'])
product.refresh_from_db()
```

**SQL запрос:**
```sql
UPDATE product 
SET remaining = remaining - 3 
WHERE id = 'uuid';
```

**Преимущества:**
- Операция выполняется на уровне БД
- Нет race condition между чтением и записью
- Гарантия атомарности

---

## Транзакции

### Зачем нужны транзакции?

```python
@transaction.atomic
def create(self, request):
    # Все операции в одной транзакции
    order.save()           # 1
    product.remaining -= 3 # 2
    product.save()         # 3
    # Если любая операция упадет - все откатится
```

**Без транзакции:**
- Заказ создан ✅
- Ошибка при обновлении остатка ❌
- Результат: заказ есть, остаток не изменился ❌

**С транзакцией:**
- Заказ создан ✅
- Ошибка при обновлении остатка ❌
- Результат: все откатилось, заказа нет ✅

---

## Тестирование

Создано 6 новых тестов в `api/tests/test_stock_restoration.py`:

| # | Тест | Описание |
|---|------|----------|
| 1 | `test_stock_restored_on_order_deletion` | Остатки восстанавливаются при удалении |
| 2 | `test_stock_not_restored_for_finished_order` | Остатки НЕ восстанавливаются для завершенных |
| 3 | `test_stock_restored_for_pending_assembly_order` | Восстановление для pending_assembly |
| 4 | `test_restore_stock_method` | Метод restore_stock() работает корректно |
| 5 | `test_multiple_products_restoration` | Восстановление нескольких товаров |
| 6 | `test_transaction_rollback_on_error` | Транзакция откатывается при ошибке |

### Запуск тестов

```bash
# Все тесты (33 штуки)
$env:TESTING="1"; python manage.py test api.tests

# Только тесты восстановления (6 штук)
$env:TESTING="1"; python manage.py test api.tests.test_stock_restoration

# Только тесты валидации (7 штук)
$env:TESTING="1"; python manage.py test api.tests.test_remaining_validation
```

**Результат:** ✅ Все 33 теста пройдены (10 моделей + 10 views + 7 остатков + 6 восстановления)

---

## Примеры использования

### Пример 1: Успешное создание заказа

```python
# Начальное состояние
product.remaining = 10

# Пользователь создает заказ на 3 товара
POST /api/orders/
# Корзина: [{product_id: uuid, amount: 3}]

# Результат
product.remaining = 7  # Уменьшилось на 3
order.status = 'pending_payment'
```

---

### Пример 2: Отмена заказа

```python
# Состояние после создания заказа
product.remaining = 7
order.status = 'pending_payment'

# Пользователь удаляет заказ
DELETE /api/orders/{order_id}/

# Результат
product.remaining = 10  # Восстановилось
order удален
```

---

### Пример 3: Неудачная оплата

```python
# Состояние после создания заказа
product.remaining = 7
order.status = 'pending_payment'

# Проверка оплаты
GET /api/orders/{order_id}/check_payment_status/?bankOrderId=123

# Ответ от банка: оплата не прошла
# Результат
product.remaining = 10  # Восстановилось
order удален
```

---

### Пример 4: Завершенный заказ

```python
# Состояние
product.remaining = 7
order.status = 'finished'

# Пользователь пытается удалить заказ
DELETE /api/orders/{order_id}/

# Результат
product.remaining = 7  # НЕ восстановилось (заказ завершен)
order удален
```

---

## Изменения в коде

### Файлы изменены

1. **api/views/OrderViewSet.py**
   - Добавлен импорт `transaction`
   - Добавлен декоратор `@transaction.atomic` к методам `create` и `delete`
   - Добавлен `select_for_update()` для блокировки строк
   - Использование `F()` для атомарных операций
   - Обновлен метод `check_payment_status` для восстановления остатков
   - Обновлен метод `delete` для условного восстановления остатков

2. **api/models.py**
   - Добавлен метод `restore_stock()` в модель `Order`

3. **api/tests/test_stock_restoration.py**
   - Создан новый файл с 6 тестами

### Строк кода добавлено

- `OrderViewSet.py`: ~20 строк
- `models.py`: ~7 строк
- `test_stock_restoration.py`: ~150 строк
- **Итого:** ~177 строк

---

## Преимущества реализации

### ✅ Надежность
- Транзакции гарантируют целостность данных
- Блокировки предотвращают race conditions
- Атомарные операции исключают промежуточные состояния

### ✅ Безопасность
- Невозможно создать заказ на недоступный товар
- Остатки не могут стать отрицательными
- Автоматическое восстановление при ошибках

### ✅ Гибкость
- Условное восстановление в зависимости от статуса
- Поддержка множества товаров в заказе
- Легко расширяется для новых сценариев

### ✅ Производительность
- Атомарные операции на уровне БД
- Минимум запросов к БД
- Оптимизация с помощью `select_related()`

---

## Возможные улучшения

### 1. Логирование изменений остатков

```python
class StockHistory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    change = models.IntegerField()  # +10 или -5
    reason = models.CharField(max_length=50)  # 'order_created', 'order_cancelled'
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
```

### 2. Резервирование товаров в корзине

```python
class Cart(models.Model):
    # ...
    reserved_until = models.DateTimeField(null=True, blank=True)
    
    def reserve(self, minutes=30):
        self.reserved_until = timezone.now() + timedelta(minutes=minutes)
        self.save()
```

### 3. Уведомления о низких остатках

```python
def check_low_stock(product):
    if product.remaining < product.min_stock_level:
        send_notification_to_admin(
            f"Товар {product.name} заканчивается! Осталось: {product.remaining}"
        )
```

### 4. Автоматическая отмена неоплаченных заказов

```python
# Celery task
@periodic_task(run_every=timedelta(hours=1))
def cancel_unpaid_orders():
    expired_orders = Order.objects.filter(
        status='pending_payment',
        datetime__lt=timezone.now() - timedelta(hours=24)
    )
    for order in expired_orders:
        order.restore_stock()
        order.status = 'cancelled'
        order.save()
```

---

## Заключение

Реализована полная система управления остатками товаров с поддержкой:

✅ **Создание заказа** - уменьшение остатков  
✅ **Отмена заказа** - восстановление остатков  
✅ **Неудачная оплата** - восстановление остатков  
✅ **Транзакции** - целостность данных  
✅ **Блокировки** - защита от race conditions  
✅ **Атомарные операции** - надежность  
✅ **Тестирование** - 33/33 тестов пройдено  

Система готова к использованию в production! 🚀

---

**Подготовлено:** Kiro AI  
**Дата:** 11 мая 2026  
**Версия:** 2.0
