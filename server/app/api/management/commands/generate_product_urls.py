"""Management-команда для генерации source_url товаров."""

from django.core.management.base import BaseCommand
from api.models.Product import Product


class Command(BaseCommand):
    """Генерирует source_url для всех товаров."""
    help = 'Генерация значений для полей source_url для товаров'

    def handle(self, *args, **options) -> None:
        """Выполняет генерацию source_url для всех товаров.
        
        Args:
            *args: Позиционные аргументы.
            **options: Именованные аргументы.
        """
        products = Product.objects.all()

        for product in products:
            product.source_url = f'https://pereulokstore.ru/products/{product.id}/'
            product.save(update_fields = ['source_url'])

        self.stdout.write("Successfully generated urls for objects 'Product'")
