import io
from uuid import UUID

from django.contrib.auth import login, logout
from django.contrib.auth.models import User, AbstractUser, AnonymousUser
from django.contrib.sessions.backends.base import SessionBase
from django.core.files import File
from django.db.models import QuerySet
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from silk.profiling.profiler import silk_profile

from .filters import ProductFilter
from .models import Product, AuthenticationRequest, Cart, Order, AuthenticationToken, UserImage
from .serializer import (
    ProductSerializer, AuthenticationRequestSerializer, CartSerializer, OrderSerializer, AuthenticationTokenSerializer,
    UserSerializer
)
from .utils import register_order, get_order_status


# noinspection PyMethodMayBeStatic,PyUnusedLocal
class Products(viewsets.ViewSet):
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    @silk_profile(name = 'Product List')
    def list(self, request: Request) -> Response:
        products = Product.objects.all().optimized()
        filterset = ProductFilter(request.query_params, queryset = products)

        if not filterset.is_valid():
            return Response(filterset.errors, status = status.HTTP_400_BAD_REQUEST)

        products_filtered = filterset.qs
        serializer = ProductSerializer(products_filtered, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    @silk_profile(name = 'Product Retrieve')
    def retrieve(self, request: Request, pk) -> Response:
        product = get_object_or_404(Product, id = pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status = status.HTTP_200_OK)

    @silk_profile(name = 'Product Create')
    def create(self, request: Request) -> Response:
        # Проверка прав администратора
        if not request.user.is_authenticated or not request.user.is_staff:
            return Response(status = status.HTTP_403_FORBIDDEN)
        
        serializer = ProductSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    @silk_profile(name = 'Product Delete')
    def delete(self, request: Request, pk) -> Response:
        product = get_object_or_404(Product, id = pk)
        product.delete()
        return Response(
            f"Product {product.id} was deleted from database",
            status = status.HTTP_204_NO_CONTENT
        )

    @silk_profile(name = 'Product Update')
    def partial_update(self, request: Request, pk) -> Response:
        # Поля для обновления
        name = request.data.get('name')
        new_type = request.data.get('type')
        price = request.data.get('price')
        description = request.data.get('description')

        data: dict[str, str] = dict()

        if name is not None: data['name'] = name
        if new_type is not None: data['type'] = new_type
        if price is not None: data['price'] = price
        if description is not None: data['description'] = description

        product: Product = get_object_or_404(Product, id = pk)
        serializer = ProductSerializer(product, data = data, partial = True)
        serializer.is_valid()
        return Response(data = serializer.data, status = status.HTTP_200_OK)


# noinspection PyMethodMayBeStatic,PyUnusedLocal
class Carts(viewsets.ViewSet):
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


# noinspection PyMethodMayBeStatic,PyUnusedLocal
class Orders(viewsets.ViewSet):
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
    def create(self, request: Request) -> Response:
        user: AbstractUser | AnonymousUser = request.user

        # Проверка авторизации
        if not user.is_authenticated:
            return Response(status = status.HTTP_403_FORBIDDEN)

        cart_items: QuerySet[Cart] = Cart.objects.all().filter(user = user)
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
    def delete(self, request: Request, pk) -> Response:
        user: AbstractUser | AnonymousUser = request.user
        order = get_object_or_404(Order, pk = pk)

        if user != order.user:
            return Response(status = status.HTTP_403_FORBIDDEN)

        order.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

    @action(methods = ['get'], detail = True, permission_classes = [IsAuthenticated])
    def check_payment_status(self, request: Request, pk) -> Response:
        bank_order_id = request.query_params.get('bankOrderId')
        order_status = get_order_status(bank_order_id)
        order = get_object_or_404(Order, pk = pk)

        if order_status == 2:
            serializer = OrderSerializer(order, data = {'status': 'pending_assembly'}, partial = True)
            serializer.is_valid(raise_exception = True)
            serializer.save()

            return Response({'paymentStatus': 'successful'}, status = status.HTTP_200_OK)
        else:
            order.delete()
            return Response({'paymentStatus': 'failure'}, status = status.HTTP_200_OK)


class UserMethods(viewsets.ViewSet):
    # noinspection PyTypeChecker
    @action(methods = ['post'], detail = False)
    def authenticate(self, request: Request) -> Response:
        # Поля данных
        token = request.data.get('token')

        authentication_request: AuthenticationRequest = get_object_or_404(AuthenticationRequest, token = token)

        user, _ = User.objects.update_or_create(
            id = authentication_request.telegram_id,
            defaults = {
                'id': authentication_request.telegram_id,
                'username': authentication_request.telegram_username,
                'first_name': authentication_request.telegram_name
            }
        )

        telegram_image_io = io.BytesIO(authentication_request.telegram_image)
        telegram_image_io.name = f'{user.id}'
        user_image, _ = UserImage.objects.update_or_create(
            user = user,
            defaults = {
                'user': user,
                'image': File(telegram_image_io)
            }
        )

        if request.user.is_authenticated:
            UserMethods.deauthenticate()

        request.session.create()
        login(request, user)
        authentication_request.token.delete()

        return Response(status = status.HTTP_200_OK)

    @action(methods = ['get'], detail = False, permission_classes = [IsAuthenticated])
    def deauthenticate(self, request: HttpRequest) -> Response:
        session: SessionBase = request.session
        logout(request)
        session.delete()
        return Response(status = status.HTTP_200_OK)

    @action(methods = ['get'], detail = False, permission_classes = [IsAuthenticated])
    def empty_user_cart(self, request: Request) -> Response:
        user: AbstractUser | AnonymousUser = request.user
        cart_items = Cart.objects.all().filter(user = user)

        for cart_item in cart_items:
            cart_item.delete()

        return Response(status = status.HTTP_204_NO_CONTENT)


class UserView(viewsets.ViewSet):
    serializer_class = UserSerializer

    @silk_profile(name = 'User Retrieve')
    def retrieve(self, request: Request) -> Response:
        user: AbstractUser | AnonymousUser = request.user
        is_authenticated: bool = user.is_authenticated

        if not is_authenticated:
            return Response(status = status.HTTP_204_NO_CONTENT)

        serializer = UserSerializer(user)
        return Response(serializer.data, status = status.HTTP_200_OK)


class AuthenticationTokenView(viewsets.ViewSet):
    serializer_class = AuthenticationTokenSerializer

    @action(methods = ['post'], detail = False)
    def create(self, request: Request) -> Response:
        # if request.user.is_authenticated:
        #     return Response(status.HTTP_400_BAD_REQUEST)

        auth_token: AuthenticationToken = AuthenticationToken.objects.create()
        return Response(data = {'token': auth_token.id}, status = status.HTTP_201_CREATED)

    @action(methods = ['delete'], detail = True)
    def destroy(self, request: Request, pk: UUID) -> Response:
        authentication_token = get_object_or_404(AuthenticationToken, pk)
        authentication_token.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)


class AuthenticationRequestView(viewsets.ViewSet):
    serializer_class = AuthenticationRequestSerializer

    @action(methods = ['post'], detail = False)
    def create(self, request: Request) -> Response:
        # Поля для создания
        data: dict[str, str | int] = {
            'token': request.data.get('token'),
            'telegram_id': request.data.get('telegram_id'),
            'telegram_username': request.data.get('telegram_username'),
            'telegram_name': request.data.get('telegram_name'),
            'telegram_image': request.FILES['telegram_image'].read()
        }

        try:
            serializer = AuthenticationRequestSerializer(data = data)
            serializer.is_valid(raise_exception = True)
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        except Exception:
            auth_token = get_object_or_404(AuthenticationToken, id = data['token'])
            auth_token.delete()
            return Response(status = status.HTTP_400_BAD_REQUEST)

    @action(methods = ['get'], detail = True)
    def retrieve(self, request: Request, pk: UUID) -> Response:
        authentication_request = get_object_or_404(AuthenticationRequest, pk = pk)
        serializer = AuthenticationRequestSerializer(authentication_request)
        return Response(serializer.data, status = status.HTTP_200_OK)

    @action(methods = ['delete'], detail = True)
    def destroy(self, request: Request, pk: UUID) -> Response:
        authentication_request = get_object_or_404(AuthenticationRequest, pk = pk)
        authentication_request.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
