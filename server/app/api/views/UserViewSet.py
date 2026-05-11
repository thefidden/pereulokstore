"""ViewSet для получения информации о пользователе."""

from django.contrib.auth.models import AbstractUser, AnonymousUser
from rest_framework import viewsets, status
from rest_framework.request import Request
from rest_framework.response import Response
from silk.profiling.profiler import silk_profile

from api.serializers.UserSerializer import UserSerializer


class UserViewSet(viewsets.ViewSet):
    """ViewSet для получения информации о текущем пользователе."""
    serializer_class = UserSerializer

    @silk_profile(name = 'User Retrieve')
    def retrieve(self, request: Request) -> Response:
        """Получает информацию о текущем пользователе.
        
        Args:
            request: HTTP запрос с данными пользователя.
            
        Returns:
            Response: Данные пользователя или 204 для неавторизованных.
        """
        user: AbstractUser | AnonymousUser = request.user
        is_authenticated: bool = user.is_authenticated

        if not is_authenticated:
            return Response(status = status.HTTP_204_NO_CONTENT)

        serializer = UserSerializer(user)
        return Response(serializer.data, status = status.HTTP_200_OK)
