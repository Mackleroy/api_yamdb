# from rest_framework import serializers
from rest_framework import serializers

from users_and_registrations.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']


class ConfirmationEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    confirmation_code = serializers.CharField()


class GetJWTTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
