from rest_framework import serializers

from api.models.Product import Product
from api.models.ProductImage import ProductImage
from api.serializers.ProductTagSerializer import ProductTagSerializer


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Product.

    Обрабатывает сериализацию товаров с изображениями, тегами и ссылками.
    Поддерживает загрузку нескольких изображений при создании товара.
    """
    images = serializers.SerializerMethodField()
    uploaded_images = serializers.ListField(
        child = serializers.ImageField(allow_empty_file = False, use_url = False),
        write_only = True,
        required = False
    )
    link = serializers.SerializerMethodField()
    product_tags = ProductTagSerializer(source = 'producttag_set', many = True, read_only = True)

    class Meta:
        model = Product
        fields = ['id', 'type', 'name', 'price', 'description', 'images', 'uploaded_images', 'link', 'product_tags', 'remaining']

    def create(self, validated_data) -> Product:
        """Создает товар с загруженными изображениями.

        Args:
            validated_data: Валидированные данные товара.

        Returns:
            Product: Созданный товар с изображениями.
        """
        uploaded_images = validated_data.pop('uploaded_images', [])
        product = Product.objects.create(**validated_data)

        for image in uploaded_images:
            ProductImage.objects.create(product = product, image = image)

        return product

    def get_images(self, obj):
        return [image.image.url for image in obj.images.all()]

    def get_link(self, obj):
        return obj.get_absolute_url()
