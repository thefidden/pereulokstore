"""Management-команда для генерации slug товаров."""

from django.core.management.base import BaseCommand
from api.models.Product import Product


class Command(BaseCommand):
    """Генерирует slug для всех товаров на основе их ID."""
    help = 'Генерация значений для полей slug для товаров'

    def handle(self, *args, **options) -> None:
        """Выполняет генерацию slug для всех товаров.
        
        Args:
            *args: Позиционные аргументы.
            **options: Именованные аргументы.
        """
        products = Product.objects.all()

        for product in products:
            product.slug = f'{product.id}'
            product.save(update_fields = ['slug'])

        self.stdout.write("Successfully generated slugs for objects 'Product'")
