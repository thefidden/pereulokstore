from rest_framework import serializers

from api.models.Order import Order
from api.models.OrderProduct import OrderProduct
from api.serializers.OrderProductSerializer import OrderProductSerializer


class OrderSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Order.

    Обрабатывает создание заказов с вложенными товарами и автоматическим
    вычислением общей стоимости.
    """
    products = OrderProductSerializer(many = True, read_only = True)
    added_products = OrderProductSerializer(many = True, write_only = True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'price', 'status', 'products', 'added_products']
        read_only_fields = ['order', 'price']

    def create(self, validated_data):
        """Создает заказ с товарами и вычисляет общую стоимость.

        Args:
            validated_data: Валидированные данные заказа с товарами.

        Returns:
            Order: Созданный заказ с товарами.
        """

        user = validated_data.pop('user')
        added_products = validated_data.pop('added_products')

        order = Order.objects.create(user = user)

        for added_product in added_products:
            product, amount = added_product['product'], added_product['amount']

            OrderProduct.objects.create(
                order = order,
                product = product,
                price = product.price,
                amount = amount
            )

            order.price += product.price * amount

        order.save()
        return order
