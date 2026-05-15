from rest_framework import serializers

from api.models.ProductTag import ProductTag
from api.serializers.TagSerializer import TagSerializer


class ProductTagSerializer(serializers.ModelSerializer):
    """Сериализатор для промежуточной модели ProductTag.

    Обрабатывает сериализацию связи товара и тега с дополнительными полями.
    """
    tag = TagSerializer(read_only = True)

    class Meta:
        model = ProductTag
        fields = ['tag', 'priority', 'added_at']
