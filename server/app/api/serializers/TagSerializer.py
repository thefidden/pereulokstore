from rest_framework import serializers

from api.models.Tag import Tag


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Tag.

    Обрабатывает сериализацию тегов товаров.
    """
    class Meta:
        model = Tag
        fields = ['name', 'slug']
