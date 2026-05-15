from django.contrib.auth.models import User
from rest_framework import serializers

from api.serializers.CartSerializer import CartSerializer
from api.serializers.OrderSerializer import OrderSerializer
from api.serializers.UserImageSerializer import UserImageSerializer


class UserSerializer(serializers.ModelSerializer):
    image = UserImageSerializer(read_only = True)
    cart = CartSerializer(many = True, read_only = True)
    orders = OrderSerializer(many = True, read_only = True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'username', 'image', 'cart', 'orders']
