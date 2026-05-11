from uuid import UUID

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from api.models import AuthenticationToken, AuthenticationRequest
from api.serializer import AuthenticationRequestSerializer


class AuthenticationRequestView(viewsets.ViewSet):
    serializer_class = AuthenticationRequestSerializer

    @action(methods = ['post'], detail = False)
    def create(self, request: Request) -> Response:
        # Поля для создания
        data: dict = {
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
