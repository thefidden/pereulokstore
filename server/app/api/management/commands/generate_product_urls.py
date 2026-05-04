from django.core.management.base import BaseCommand
from api.models import Product


class Command(BaseCommand):
    help = 'Генерация значений для полей source_url для товаров'

    def handle(self, *args, **options) -> None:
        products = Product.objects.all()

        for product in products:
            product.source_url = f'https://pereulokstore.ru/products/{product.id}/'
            product.save(update_fields = ['source_url'])

        self.stdout.write("Successfully generated urls for objects 'Product'")
