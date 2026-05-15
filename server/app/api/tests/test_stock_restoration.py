"""Тесты возврата товаров на склад при отмене заказа."""

from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from api.models.OrderProduct import OrderProduct
from api.models.Order import Order
from api.models.Cart import Cart
from api.models.Product import Product


class StockRestorationTest(APITestCase):
    """Тесты восстановления остатков товаров."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('testuser', password = 'testpass')
        
        # Товар с ограниченным остатком
        self.product = Product.objects.create(
            name = "Test Product",
            type = "suit",
            price = 1000,
            description = "Test",
            remaining = 10
        )

    def test_stock_restored_on_order_deletion(self):
        """Тест 1: Остатки восстанавливаются при удалении заказа."""
        self.client.force_authenticate(user = self.user)
        
        # Создаем заказ (остаток должен уменьшиться)
        Cart.objects.create(user = self.user, product = self.product, amount = 3)
        response = self.client.post('/api/orders/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        order_id = response.data['order']['id']
        
        # Проверяем, что остаток уменьшился
        self.product.refresh_from_db()
        self.assertEqual(self.product.remaining, 7)
        
        # Удаляем заказ
        response = self.client.delete(f'/api/orders/{order_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Проверяем, что остаток восстановился
        self.product.refresh_from_db()
        self.assertEqual(self.product.remaining, 10)

    def test_stock_not_restored_for_finished_order(self):
        """Тест 2: Остатки НЕ восстанавливаются для завершенных заказов."""
        self.client.force_authenticate(user = self.user)
        
        # Создаем заказ
        Cart.objects.create(user = self.user, product = self.product, amount = 3)
        response = self.client.post('/api/orders/')
        order_id = response.data['order']['id']
        
        # Меняем статус на "завершен"
        order = Order.objects.get(id = order_id)
        order.status = 'finished'
        order.save()
        
        # Проверяем остаток до удаления
        self.product.refresh_from_db()
        self.assertEqual(self.product.remaining, 7)
        
        # Удаляем заказ
        response = self.client.delete(f'/api/orders/{order_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Проверяем, что остаток НЕ восстановился (заказ был завершен)
        self.product.refresh_from_db()
        self.assertEqual(self.product.remaining, 7)

    def test_stock_restored_for_pending_assembly_order(self):
        """Тест 3: Остатки восстанавливаются для заказов в статусе 'pending_assembly'."""
        self.client.force_authenticate(user = self.user)
        
        # Создаем заказ
        Cart.objects.create(user = self.user, product = self.product, amount = 3)
        response = self.client.post('/api/orders/')
        order_id = response.data['order']['id']
        
        # Меняем статус на "собирается"
        order = Order.objects.get(id = order_id)
        order.status = 'pending_assembly'
        order.save()
        
        # Удаляем заказ
        response = self.client.delete(f'/api/orders/{order_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Проверяем, что остаток восстановился
        self.product.refresh_from_db()
        self.assertEqual(self.product.remaining, 10)

    def test_restore_stock_method(self):
        """Тест 4: Метод restore_stock() корректно возвращает товары."""
        # Создаем заказ вручную
        order = Order.objects.create(user = self.user, price = 3000)
        OrderProduct.objects.create(
            order = order,
            product = self.product,
            price = self.product.price,
            amount = 3
        )
        
        # Уменьшаем остаток вручную
        self.product.remaining = 7
        self.product.save()
        
        # Вызываем метод restore_stock
        order.restore_stock()
        
        # Проверяем, что остаток восстановился
        self.product.refresh_from_db()
        self.assertEqual(self.product.remaining, 10)

    def test_multiple_products_restoration(self):
        """Тест 5: Восстановление остатков для нескольких товаров."""
        self.client.force_authenticate(user = self.user)
        
        # Создаем второй товар
        product2 = Product.objects.create(
            name = "Test Product 2",
            type = "suit",
            price = 2000,
            description = "Test",
            remaining = 20
        )
        
        # Добавляем оба товара в корзину
        Cart.objects.create(user = self.user, product = self.product, amount = 3)
        Cart.objects.create(user = self.user, product = product2, amount = 5)
        
        # Создаем заказ
        response = self.client.post('/api/orders/')
        order_id = response.data['order']['id']
        
        # Проверяем, что остатки уменьшились
        self.product.refresh_from_db()
        product2.refresh_from_db()
        self.assertEqual(self.product.remaining, 7)
        self.assertEqual(product2.remaining, 15)
        
        # Удаляем заказ
        self.client.delete(f'/api/orders/{order_id}/')
        
        # Проверяем, что остатки восстановились
        self.product.refresh_from_db()
        product2.refresh_from_db()
        self.assertEqual(self.product.remaining, 10)
        self.assertEqual(product2.remaining, 20)

    def test_transaction_rollback_on_error(self):
        """Тест 6: Транзакция откатывается при ошибке."""
        self.client.force_authenticate(user = self.user)
        
        # Добавляем товар в корзину
        Cart.objects.create(user = self.user, product = self.product, amount = 3)
        
        # Проверяем начальный остаток
        initial_remaining = self.product.remaining
        
        # Пытаемся создать заказ (должно пройти успешно)
        response = self.client.post('/api/orders/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Проверяем, что остаток изменился
        self.product.refresh_from_db()
        self.assertEqual(self.product.remaining, initial_remaining - 3)
