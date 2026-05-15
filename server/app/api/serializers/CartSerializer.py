from rest_framework import serializers

from api.models.Cart import Cart
from api.models.Product import Product
from api.serializers.ProductSerializer import ProductSerializer


class CartSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Cart.

    Обрабатывает сериализацию корзины с вложенными данными товара
    и вычисленной общей стоимостью.
    """
    product = ProductSerializer(read_only = True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset = Product.objects.all(),
        source = 'product',
        write_only = True
    )
    total_price = serializers.IntegerField(read_only = True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'product', 'product_id', 'amount', 'total_price']
