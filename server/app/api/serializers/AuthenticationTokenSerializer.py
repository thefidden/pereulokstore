from rest_framework import serializers

from api.models.AuthenticationToken import AuthenticationToken


class AuthenticationTokenSerializer(serializers.ModelSerializer):
    """Сериализатор для модели AuthenticationToken.

    Обрабатывает сериализацию токенов аутентификации.
    """
    class Meta:
        model = AuthenticationToken
        fields = ['id']
