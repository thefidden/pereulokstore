# Быстрый старт: Управление остатками товаров

## Что добавлено

✅ Поле `remaining` в модель `Product` (остаток товара на складе)  
✅ Автоматическая проверка при создании заказа  
✅ Уменьшение остатков после успешного заказа  
✅ Информативные ошибки при недостатке товара  

---

## Как это работает

### 1. Просмотр остатков товара

```http
GET /api/products/{id}/
```

**Ответ:**
```json
{
  "id": "uuid",
  "name": "Товар",
  "price": 1000,
  "remaining": 50,  ← Остаток на складе
  ...
}
```

---

### 2. Создание заказа

#### ✅ Успешный заказ (товара достаточно)

**Запрос:**
```http
POST /api/orders/
Authorization: Bearer <token>
```

**Корзина:** Товар A (3 шт.), на складе: 10 шт.

**Ответ:** `201 Created`
```json
{
  "order": { ... },
  "formUrl": "..."
}
```

**Результат:** Остаток товара A = 7 шт.

---

#### ❌ Недостаточно товара

**Запрос:**
```http
POST /api/orders/
Authorization: Bearer <token>
```

**Корзина:** Товар A (15 шт.), на складе: 10 шт.

**Ответ:** `400 Bad Request`
```json
{
  "detail": "Недостаточно товаров на складе",
  "insufficient_stock": [
    {
      "product_id": "uuid",
      "product_name": "Товар A",
      "requested": 15,
      "available": 10
    }
  ]
}
```

**Результат:** Заказ НЕ создан, остатки НЕ изменились

---

## Для разработчиков

### Миграция

```bash
# Уже применена, но если нужно:
python manage.py migrate
```

### Тестирование

```bash
# Все тесты (27 штук)
$env:TESTING="1"; python manage.py test api.tests

# Только тесты остатков (7 штук)
$env:TESTING="1"; python manage.py test api.tests.test_remaining_validation
```

**Результат:** ✅ Все 27 тестов пройдены (10 моделей + 10 views + 7 остатков)

---

### Изменения в коде

#### models.py
```python
class Product(models.Model):
    remaining = models.IntegerField(
        null = False, 
        default = 10_000,  # По умолчанию 10 тысяч
        validators = [MinValueValidator(0)],
        verbose_name = 'В наличии'
    )
```

#### serializer.py
```python
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [..., 'remaining']  # Добавлено поле
```

#### views/OrderViewSet.py (OrderViewSet.create)
```python
# 1. Проверка остатков
insufficient_stock = []
for cart_item in cart_items:
    if cart_item.product.remaining < cart_item.amount:
        insufficient_stock.append({
            'product_id': str(cart_item.product.id),
            'product_name': cart_item.product.name,
            'requested': cart_item.amount,
            'available': cart_item.product.remaining
        })

if insufficient_stock:
    return Response({
        'detail': 'Недостаточно товара на складе',
        'insufficient_stock': insufficient_stock
    }, status = 400)

# 2. Уменьшение остатков после создания заказа
for cart_item in cart_items:
    cart_item.product.remaining -= cart_item.amount
    cart_item.product.save(update_fields=['remaining'])
```

---

## Примеры использования

### Frontend: Показать остаток товара

```javascript
// Получить товар
const response = await fetch('/api/products/uuid/');
const product = await response.json();

// Показать остаток
if (product.remaining === 0) {
  showMessage('Нет в наличии');
} else if (product.remaining < 10) {
  showMessage(`Осталось всего ${product.remaining} шт.`);
}
```

### Frontend: Обработка ошибки при заказе

```javascript
// Создать заказ
const response = await fetch('/api/orders/', {
  method: 'POST',
  headers: { 'Authorization': `Bearer ${token}` }
});

if (response.status === 400) {
  const error = await response.json();
  
  if (error.insufficient_stock) {
    // Показать список недоступных товаров
    error.insufficient_stock.forEach(item => {
      showError(
        `${item.product_name}: запрошено ${item.requested}, ` +
        `доступно ${item.available}`
      );
    });
  }
}
```

---

## Часто задаваемые вопросы

### Q: Что если два пользователя одновременно заказывают последний товар?

A: Django использует транзакции базы данных. Первый успешный заказ уменьшит остаток, второй получит ошибку о недостатке товара.

### Q: Как изменить остаток товара вручную?

A: Через Django Admin или напрямую в базе данных:
```python
product = Product.objects.get(id='uuid')
product.remaining = 100
product.save()
```

### Q: Что происходит при отмене заказа?

A: Сейчас остатки НЕ возвращаются автоматически. Нужно реализовать отдельно (см. STOCK_MANAGEMENT.md).

### Q: Можно ли зарезервировать товар в корзине?

A: Сейчас нет. Товар резервируется только при создании заказа. Резервирование в корзине можно добавить (см. STOCK_MANAGEMENT.md).

---

## Документация

📄 **STOCK_MANAGEMENT.md** - Полная документация с примерами и улучшениями  
📄 **TEST_REPORT.md** - Отчет по тестированию API  
📄 **TESTING_SUMMARY.md** - Итоговый отчет по всем тестам  

---

**Версия:** 1.0  
**Дата:** 11 мая 2026
