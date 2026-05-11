from rest_framework import serializers

from api.models.AuthenticationRequest import AuthenticationRequest


class AuthenticationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthenticationRequest
        fields = ['token', 'telegram_id', 'telegram_username', 'telegram_name', 'telegram_image']
