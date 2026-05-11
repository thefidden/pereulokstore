"""Тесты моделей API."""

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db import IntegrityError
from api.models import Product, Cart, Order, OrderProduct, Tag, ProductTag


class ProductModelTest(TestCase):
    """Тесты модели Product."""

    def test_create_product_with_valid_data(self):
        """Тест 1: Создание товара с валидными данными."""
        product = Product.objects.create(
            name = "Test Product",
            type = "suit",
            price = 1000,
            description = "Test description"
        )

        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.price, 1000)
        self.assertIsNotNone(product.id)
        self.assertIsNotNone(product.slug)

    def test_product_slug_auto_generated(self):
        """Тест 2: Автоматическая генерация slug."""
        product = Product.objects.create(
            name = "Test",
            type = "suit",
            price = 100,
            description = "Test"
        )

        # Slug должен быть равен UUID
        self.assertEqual(str(product.slug), str(product.id))

    def test_product_source_url_auto_generated(self):
        """Тест 3: Автоматическая генерация source_url."""
        product = Product.objects.create(
            name = "Test",
            type = "suit",
            price = 100,
            description = "Test"
        )

        self.assertIn('pereulokstore', product.source_url)
        self.assertIn(str(product.id), product.source_url)

    def test_product_price_validation(self):
        """Тест 4: Валидация цены товара."""
        product = Product(
            name = "Test",
            type = "suit",
            price = 150000,  # Превышает MaxValueValidator(100_000)
            description = "Test"
        )

        with self.assertRaises(ValidationError):
            product.full_clean()


class CartModelTest(TestCase):
    """Тесты модели Cart."""

    def setUp(self):
        self.user = User.objects.create_user('testuser', password = 'testpass')
        self.product = Product.objects.create(
            name = "Test Product",
            type = "suit",
            price = 1000,
            description = "Test"
        )

    def test_unique_user_product_constraint(self):
        """Тест 5: Ограничение уникальности user + product."""
        Cart.objects.create(user = self.user, product = self.product, amount = 1)

        # Попытка создать дубликат должна вызывать ошибку
        with self.assertRaises(IntegrityError):
            Cart.objects.create(user = self.user, product = self.product, amount = 2)

    def test_cart_total_price_annotation(self):
        """Тест 6: Аннотация total_price."""
        Cart.objects.create(user = self.user, product = self.product, amount = 3)

        cart_item = Cart.objects.include_total_price().first()
        self.assertEqual(cart_item.total_price, 3000)  # 3 * 1000


class OrderModelTest(TestCase):
    """Тесты модели Order."""

    def setUp(self):
        self.user = User.objects.create_user('testuser', password = 'testpass')

    def test_order_default_status(self):
        """Тест 7: Статус заказа по умолчанию."""
        order = Order.objects.create(user = self.user, price = 0)

        self.assertEqual(order.status, 'pending_payment')

    def test_order_price_calculation(self):
        """Тест 8: Вычисление цены заказа."""
        product1 = Product.objects.create(name = "P1", type = "suit", price = 1000, description = "Test")
        product2 = Product.objects.create(name = "P2", type = "shape", price = 2000, description = "Test")

        order = Order.objects.create(user = self.user, price = 0)
        OrderProduct.objects.create(order = order, product = product1, price = product1.price, amount = 2)
        OrderProduct.objects.create(order = order, product = product2, price = product2.price, amount = 1)

        order.price = sum(op.price * op.amount for op in order.products.all())
        order.save()

        self.assertEqual(order.price, 4000)  # 2*1000 + 1*2000


class TagModelTest(TestCase):
    """Тесты модели Tag."""

    def test_tag_slug_auto_generated(self):
        """Тест 9: Автоматическая генерация slug для тега."""
        tag = Tag.objects.create(name = "Новинка")

        self.assertIsNotNone(tag.slug)
        self.assertTrue(len(tag.slug) > 0)

    def test_product_tag_through_model(self):
        """Тест 10: ManyToMany через промежуточную модель ProductTag."""
        product = Product.objects.create(name = "Test", type = "suit", price = 100, description = "Test")
        tag = Tag.objects.create(name = "Sale")

        ProductTag.objects.create(product = product, tag = tag, priority = 10)

        self.assertEqual(product.tags.count(), 1)
        self.assertEqual(tag.products.count(), 1)

        # Проверка дополнительного поля priority
        product_tag = ProductTag.objects.get(product = product, tag = tag)
        self.assertEqual(product_tag.priority, 10)
