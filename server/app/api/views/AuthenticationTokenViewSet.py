from uuid import UUID

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from api.models import AuthenticationToken
from api.serializer import AuthenticationTokenSerializer


class AuthenticationTokenViewSet(viewsets.ViewSet):
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
