"""Тесты проверки остатков товаров на складе."""

from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from api.models import Product, Cart


class StockValidationTest(APITestCase):
    """Тесты валидации остатков товаров."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('testuser', password = 'testpass')
        
        # Товар с ограниченным остатком
        self.product_limited = Product.objects.create(
            name = "Limited Product",
            type = "suit",
            price = 1000,
            description = "Test",
            remaining = 5
        )
        
        # Товар без остатка
        self.product_out_of_stock = Product.objects.create(
            name = "Out of Stock Product",
            type = "suit",
            price = 2000,
            description = "Test",
            remaining = 0
        )
        
        # Товар с большим остатком
        self.product_in_stock = Product.objects.create(
            name = "In Stock Product",
            type = "suit",
            price = 1500,
            description = "Test",
            remaining = 100
        )

    def test_create_order_with_sufficient_stock(self):
        """Тест 1: Создание заказа при достаточном количестве товара."""
        self.client.force_authenticate(user = self.user)
        
        # Добавляем товар в корзину (3 штуки, есть 5)
        Cart.objects.create(user = self.user, product = self.product_limited, amount = 3)
        
        response = self.client.post('/api/orders/')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Проверяем, что остаток уменьшился
        self.product_limited.refresh_from_db()
        self.assertEqual(self.product_limited.remaining, 2)

    def test_create_order_with_insufficient_stock(self):
        """Тест 2: Создание заказа при недостаточном количестве товара."""
        self.client.force_authenticate(user = self.user)
        
        # Добавляем товар в корзину (10 штук, есть только 5)
        Cart.objects.create(user = self.user, product = self.product_limited, amount = 10)
        
        response = self.client.post('/api/orders/')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Проверяем, что остаток НЕ изменился
        self.product_limited.refresh_from_db()
        self.assertEqual(self.product_limited.remaining, 5)

    def test_create_order_with_out_of_stock_product(self):
        """Тест 3: Создание заказа с товаром, которого нет в наличии."""
        self.client.force_authenticate(user = self.user)
        
        # Добавляем товар без остатка
        Cart.objects.create(user = self.user, product = self.product_out_of_stock, amount = 1)
        
        response = self.client.post('/api/orders/')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('insufficient_stock', response.data)
        self.assertEqual(response.data['insufficient_stock'][0]['available'], 0)

    def test_create_order_with_multiple_products_mixed_stock(self):
        """Тест 4: Создание заказа с несколькими товарами (один недоступен)."""
        self.client.force_authenticate(user = self.user)
        
        # Добавляем товары: один доступен, другой нет
        Cart.objects.create(user = self.user, product = self.product_in_stock, amount = 2)
        Cart.objects.create(user = self.user, product = self.product_limited, amount = 10)
        
        response = self.client.post('/api/orders/')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('insufficient_stock', response.data)
        
        # Только один товар должен быть в списке недоступных
        self.assertEqual(len(response.data['insufficient_stock']), 1)
        self.assertEqual(response.data['insufficient_stock'][0]['product_name'], "Limited Product")
        
        # Остатки НЕ должны измениться
        self.product_in_stock.refresh_from_db()
        self.product_limited.refresh_from_db()
        self.assertEqual(self.product_in_stock.remaining, 100)
        self.assertEqual(self.product_limited.remaining, 5)

    def test_create_order_with_multiple_products_all_available(self):
        """Тест 5: Создание заказа с несколькими товарами (все доступны)."""
        self.client.force_authenticate(user = self.user)
        
        # Добавляем товары: оба доступны
        Cart.objects.create(user = self.user, product = self.product_in_stock, amount = 10)
        Cart.objects.create(user = self.user, product = self.product_limited, amount = 3)
        
        response = self.client.post('/api/orders/')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Проверяем, что остатки уменьшились
        self.product_in_stock.refresh_from_db()
        self.product_limited.refresh_from_db()
        self.assertEqual(self.product_in_stock.remaining, 90)
        self.assertEqual(self.product_limited.remaining, 2)

    def test_product_remaining_in_api_response(self):
        """Тест 6: Поле remaining присутствует в API ответе."""
        response = self.client.get(f'/api/products/{self.product_limited.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('remaining', response.data)
        self.assertEqual(response.data['remaining'], 5)

    def test_product_list_shows_remaining(self):
        """Тест 7: Список товаров показывает остатки."""
        response = self.client.get('/api/products/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Проверяем, что у всех товаров есть поле remaining
        for product in response.data:
            self.assertIn('remaining', product)
