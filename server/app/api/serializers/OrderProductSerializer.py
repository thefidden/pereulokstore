from rest_framework import serializers

from api.models.OrderProduct import OrderProduct
from api.models.Product import Product
from api.serializers.ProductSerializer import ProductSerializer


class OrderProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only = True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset = Product.objects.all(),
        source = 'product',
        write_only = True
    )

    class Meta:
        model = OrderProduct
        fields = ['order', 'product', 'product_id', 'price', 'amount']
        read_only_fields = ['order', 'price']
