from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import LoginHistory
import django.contrib.auth.password_validation as validators
from django.core.exceptions import ValidationError

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password')

    def validate_password(self, value):
        try:
            validators.validate_password(value)
        except ValidationError as exc:
            raise serializers.ValidationError(list(exc.messages))
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user


class LoginHistorySerializer(serializers.ModelSerializer):
    login_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = LoginHistory
        fields = ('id', 'login_time')