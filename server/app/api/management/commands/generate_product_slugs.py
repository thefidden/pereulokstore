from django.core.management.base import BaseCommand
from api.models import Product


class Command(BaseCommand):
    help = 'Генерация значений для полей slug для товаров'

    def handle(self, *args, **options) -> None:
        products = Product.objects.all()

        for product in products:
            product.slug = f'{product.id}'
            product.save(update_fields = ['slug'])

        self.stdout.write("Successfully generated slugs for objects 'Product'")
