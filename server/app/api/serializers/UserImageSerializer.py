from rest_framework import serializers

from api.models.UserImage import UserImage


class UserImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserImage
        fields = ['user', 'image']
