from django.contrib.auth.models import AbstractUser, AnonymousUser
from django.db import transaction
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from silk.profiling.profiler import silk_profile

from api.models import Order, Cart
from api.serializer import OrderSerializer
from api.utils import register_order, get_order_status


class OrderViewSet(viewsets.ViewSet):
    serializer_class = OrderSerializer

    @silk_profile(name = 'Orders List')
    def list(self, request: Request) -> Response:
        user = request.user

        if not user.is_authenticated:
            return Response(data = [], status = status.HTTP_204_NO_CONTENT)

        orders = Order.objects.user_orders(user).optimized()
        serializer = OrderSerializer(orders, many = True)
        return Response(data = serializer.data,
                        status = status.HTTP_200_OK if serializer.data else status.HTTP_204_NO_CONTENT)

    @silk_profile(name = 'Orders')
    @transaction.atomic
    def create(self, request: Request) -> Response:
        user: AbstractUser | AnonymousUser = request.user

        # Проверка авторизации
        if not user.is_authenticated:
            return Response(status = status.HTTP_403_FORBIDDEN)

        # Получаем товары из корзины с блокировкой для предотвращения race conditions
        cart_items: QuerySet[Cart] = (
            Cart.objects
            .user_items(user)
            .select_related('product')
            .select_for_update()
        )

        # Проверка наличия товаров на складе
        insufficient_stock = []
        for cart_item in cart_items:
            if cart_item.product.remaining < cart_item.amount:
                insufficient_stock.append({
                    'product_id': str(cart_item.product.id),
                    'product_name': cart_item.product.name,
                    'requested': cart_item.amount,
                    'available': cart_item.product.remaining
                })
        
        if insufficient_stock:
            return Response(
                data = {
                    'detail': 'Недостаточно товара на складе',
                    'insufficient_stock': insufficient_stock
                },
                status = status.HTTP_400_BAD_REQUEST
            )

        added_products: list[dict] = [
            {
                'product_id': cart_item.product.id,
                'amount': cart_item.amount
            }
            for cart_item in cart_items
        ]

        data = {
            'user': user.id,
            'added_products': added_products
        }

        order_serializer = OrderSerializer(data = data)

        if not order_serializer.is_valid():
            print(order_serializer.errors)

        order_serializer.is_valid(raise_exception = True)
        order_serializer.save()

        # Уменьшаем остаток товаров после успешного создания заказа
        # Используем F() для атомарного обновления
        from django.db.models import F
        for cart_item in cart_items:
            # Атомарное уменьшение остатка
            cart_item.product.remaining = F('remaining') - cart_item.amount
            cart_item.product.save(update_fields = ['remaining'])
            # Обновляем объект для получения актуального значения
            cart_item.product.refresh_from_db()

        order: Order = get_object_or_404(Order, id = order_serializer.data.get('id'))
        form_url: str = register_order(order)

        return Response({'order': order_serializer.data, 'formUrl': form_url}, status = status.HTTP_201_CREATED)

    @silk_profile(name = 'Cart Retrieve')
    def retrieve(self, request: Request, pk) -> Response:
        user: AbstractUser | AnonymousUser = request.user
        order = get_object_or_404(Order, pk = pk)

        if user != order.user:
            return Response(status = status.HTTP_403_FORBIDDEN)

        serializer = OrderSerializer(order)
        return Response(data = serializer.data, status = status.HTTP_200_OK)

    @silk_profile(name = 'Cart Delete')
    @transaction.atomic
    def delete(self, request: Request, pk) -> Response:
        user: AbstractUser | AnonymousUser = request.user
        order = get_object_or_404(Order, pk = pk)

        if user != order.user:
            return Response(status = status.HTTP_403_FORBIDDEN)

        # Возвращаем товары на склад только если заказ еще не завершен
        if order.status in ['pending_payment', 'pending_assembly']:
            order.restore_stock()
        
        order.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

    @action(methods = ['get'], detail = True, permission_classes = [IsAuthenticated])
    def check_payment_status(self, request: Request, pk) -> Response:
        bank_order_id = request.query_params.get('bankOrderId')
        order_status = get_order_status(bank_order_id)
        order = get_object_or_404(Order, pk = pk)

        if order_status == 2:
            # Оплата успешна - обновляем статус заказа
            serializer = OrderSerializer(order, data = {'status': 'pending_assembly'}, partial = True)
            serializer.is_valid(raise_exception = True)
            serializer.save()

            return Response({'paymentStatus': 'successful'}, status = status.HTTP_200_OK)
        else:
            # Оплата не прошла - возвращаем товары на склад и удаляем заказ
            order.restore_stock()
            order.delete()
            return Response({'paymentStatus': 'failure'}, status = status.HTTP_200_OK)
