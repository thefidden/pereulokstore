"""Тесты API views."""

from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from api.models import Product, Cart, Order


class ProductAPITest(APITestCase):
    """Тесты API товаров."""

    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_superuser('admin', email = 'admin@test.com', password = 'admin')
        self.product = Product.objects.create(
            name = "Test Product",
            type = "suit",
            price = 1000,
            description = "Test"
        )

    def test_list_products_public(self):
        """Тест 1: Просмотр каталога без авторизации."""
        response = self.client.get('/api/products/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_retrieve_product_public(self):
        """Тест 2: Просмотр товара без авторизации."""
        response = self.client.get(f'/api/products/{self.product.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Test Product")

    def test_create_product_requires_admin(self):
        """Тест 3: Создание товара требует прав администратора."""
        response = self.client.post('/api/products/', {
            'name': 'New Product',
            'type': 'suit',
            'price': 500,
            'description': 'Test'
        })

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_product_by_admin(self):
        """Тест 4: Создание товара администратором."""
        self.client.force_authenticate(user = self.admin)

        response = self.client.post('/api/products/', {
            'name': 'New Product',
            'type': 'suit',
            'price': 500,
            'description': 'Test'
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)


class CartAPITest(APITestCase):
    """Тесты API корзины."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('testuser', password = 'testpass')
        self.product = Product.objects.create(
            name = "Test Product",
            type = "suit",
            price = 1000,
            description = "Test"
        )

    def test_add_to_cart_requires_auth(self):
        """Тест 5: Добавление в корзину требует авторизации."""
        response = self.client.post('/api/carts/', {
            'productId': str(self.product.id)
        })

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_to_cart_authenticated(self):
        """Тест 6: Добавление товара в корзину авторизованным пользователем."""
        self.client.force_authenticate(user = self.user)

        response = self.client.post('/api/carts/', {
            'productId': str(self.product.id)
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cart.objects.count(), 1)

    def test_list_cart_items_authenticated(self):
        """Тест 7: Получение корзины авторизованным пользователем."""
        Cart.objects.create(user = self.user, product = self.product, amount = 2)
        self.client.force_authenticate(user = self.user)

        response = self.client.get('/api/carts/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        # Проверка аннотации total_price
        self.assertIn('total_price', response.data[0])
        self.assertEqual(response.data[0]['total_price'], 2000)


class OrderAPITest(APITestCase):
    """Тесты API заказов."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('testuser', password = 'testpass')
        self.product = Product.objects.create(
            name = "Test Product",
            type = "suit",
            price = 1000,
            description = "Test"
        )

    def test_create_order_requires_auth(self):
        """Тест 8: Создание заказа требует авторизации."""
        response = self.client.post('/api/orders/')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_orders_authenticated(self):
        """Тест 9: Получение списка заказов авторизованным пользователем."""
        Order.objects.create(user = self.user, price = 1000)
        self.client.force_authenticate(user = self.user)

        response = self.client.get('/api/orders/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_retrieve_order_owner_only(self):
        """Тест 10: Просмотр заказа только владельцем."""
        order = Order.objects.create(user = self.user, price = 1000)
        other_user = User.objects.create_user('other', password = 'pass')

        self.client.force_authenticate(user = other_user)
        response = self.client.get(f'/api/orders/{order.id}/')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
