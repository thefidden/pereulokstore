import io

from django.contrib.auth import login, logout
from django.contrib.auth.models import User, AbstractUser, AnonymousUser
from django.contrib.sessions.backends.base import SessionBase
from django.core.files import File
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from api.models import AuthenticationRequest, UserImage, Cart


class UserMethodsViewSet(viewsets.ViewSet):
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
            UserMethodsViewSet.deauthenticate()

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
