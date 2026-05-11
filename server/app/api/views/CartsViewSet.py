from django.contrib.auth.models import AbstractUser, AnonymousUser
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.request import Request
from rest_framework.response import Response
from silk.profiling.profiler import silk_profile

from api.models import Cart
from api.serializer import CartSerializer


class CartsViewSet(viewsets.ViewSet):
    serializer_class = CartSerializer

    @silk_profile(name = 'Cart List')
    def list(self, request: Request) -> Response:
        # Поля для фильтров
        user = request.user

        if not user.is_authenticated:
            return Response(data = [], status = status.HTTP_204_NO_CONTENT)

        cart_items = Cart.objects.user_items(user).include_total_price().optimized()
        serializer = CartSerializer(cart_items, many = True)
        data = serializer.data

        return Response(data = data, status = status.HTTP_200_OK)

    @silk_profile(name = 'Cart Create')
    def create(self, request: Request) -> Response:
        # Проверка авторизации
        if not request.user.is_authenticated:
            return Response(
                {'detail': 'Authentication credentials were not provided.'},
                status = status.HTTP_403_FORBIDDEN
            )

        data = {
            'user': request.user.id,
            'product_id': request.data.get('productId')
        }

        serializer: CartSerializer = CartSerializer(data = data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data, status = status.HTTP_201_CREATED)

    @silk_profile(name = 'Cart Retrieve')
    def retrieve(self, request: Request, pk) -> Response:
        user_products_in_cart = get_object_or_404(Cart, pk = pk)
        serializer = CartSerializer(user_products_in_cart)
        return Response(data = serializer.data, status = status.HTTP_200_OK)

    @silk_profile(name = 'Cart Update')
    def partial_update(self, request: Request, pk) -> Response:
        # Поля для обновления
        amount = request.data.get('amount')

        data: dict[str, str] = dict()
        if amount is not None: data['amount'] = amount

        product_in_cart = get_object_or_404(Cart, pk = pk)
        serializer = CartSerializer(product_in_cart, data = data, partial = True)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(data = serializer.data, status = status.HTTP_200_OK)

    @silk_profile(name = 'Cart Delete')
    def delete(self, request: Request, pk) -> Response:
        user: AbstractUser | AnonymousUser = request.user
        cart_item = get_object_or_404(Cart, pk = pk)

        if cart_item.user != request.user:
            return Response(status = status.HTTP_403_FORBIDDEN)

        cart_item.delete()
        return Response(
            data = f"Product {cart_item.product} was deleted from user {cart_item.user}'s cart",
            status = status.HTTP_204_NO_CONTENT
        )
