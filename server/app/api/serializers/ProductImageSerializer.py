from rest_framework import serializers

from api.models.ProductImage import ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    """Сериализатор для модели ProductImage.

    Обрабатывает сериализацию изображений товаров.
    """
    class Meta:
        model = ProductImage
        fields = ['product', 'image']
