import pprint

from rest_framework import serializers
from django.contrib.auth.models import User

from .models import (
    Product, ProductImage, AuthenticationRequest, Cart, Order, OrderProduct, AuthenticationToken, UserImage
)


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['product', 'image']


class ProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    uploaded_images = serializers.ListField(
        child = serializers.ImageField(allow_empty_file = False, use_url = False),
        write_only = True
    )
    link = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'type', 'name', 'price', 'description', 'images', 'uploaded_images', 'link']

    def create(self, validated_data) -> Product:
        uploaded_images = validated_data.pop('uploaded_images')
        product = Product.objects.create(**validated_data)

        for image in uploaded_images:
            ProductImage.objects.create(product = product, image = image)

        return product

    def get_images(self, obj):
        return [image.image.url for image in obj.images.all()]

    def get_link(self, obj):
        return obj.get_absolute_url()


class AuthenticationTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthenticationToken
        fields = ['id']


class AuthenticationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthenticationRequest
        fields = ['token', 'telegram_id', 'telegram_username', 'telegram_name', 'telegram_image']


class CartSerializer(serializers.ModelSerializer):
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


class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many = True, read_only = True)
    added_products = OrderProductSerializer(many = True, write_only = True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'price', 'status', 'products', 'added_products']
        read_only_fields = ['order', 'price']

    def create(self, validated_data):
        pprint.pprint(validated_data, indent = 4)

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


class UserImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserImage
        fields = ['user', 'image']


class UserSerializer(serializers.ModelSerializer):
    image = UserImageSerializer(read_only = True)
    cart = CartSerializer(many = True, read_only = True)
    orders = OrderSerializer(many = True, read_only = True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'username', 'image', 'cart', 'orders']
