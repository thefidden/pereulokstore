"""ViewSet для управления токенами аутентификации."""

from uuid import UUID

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from api.models.AuthenticationToken import AuthenticationToken
from api.serializers.AuthenticationTokenSerializer import AuthenticationTokenSerializer


class AuthenticationTokenViewSet(viewsets.ViewSet):
    """ViewSet для создания и удаления токенов аутентификации.
    
    Используется в процессе аутентификации через Telegram.
    """
    serializer_class = AuthenticationTokenSerializer

    @action(methods = ['post'], detail = False)
    def create(self, request: Request) -> Response:
        """Создает новый токен аутентификации.
        
        Args:
            request: HTTP запрос.
            
        Returns:
            Response: ID созданного токена.
        """
        auth_token: AuthenticationToken = AuthenticationToken.objects.create()
        return Response(data = {'token': auth_token.id}, status = status.HTTP_201_CREATED)

    @action(methods = ['delete'], detail = True)
    def destroy(self, request: Request, pk: UUID) -> Response:
        """Удаляет токен аутентификации.
        
        Args:
            request: HTTP запрос.
            pk: ID токена.
            
        Returns:
            Response: 204 при успешном удалении или 404.
        """
        authentication_token = get_object_or_404(AuthenticationToken, pk)
        authentication_token.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
