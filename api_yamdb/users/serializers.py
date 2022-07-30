from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        lookup_field = 'username'


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate(self, attrs):
        if attrs.get('username') == 'me':
            raise ValidationError(
                {'username': 'Имя пользователя не может быть "me"'}
            )
        username_user = User.objects.filter(
            username=attrs.get('username')
        ).exists()
        email_user = User.objects.filter(
            email=attrs.get('email')
        ).exists()
        same_user = User.objects.filter(
            username=attrs.get('username'),
            email=attrs.get('email'),
        ).exists()
        if username_user and email_user and not same_user:
            raise serializers.ValidationError(
                {'username': 'Данный логин уже занят',
                 'email': 'Данная почта уже занята'}
            )
        if username_user and not same_user:
            raise serializers.ValidationError(
                {'username': 'Данный логин уже занят'}
            )
        if email_user and not same_user:
            raise serializers.ValidationError(
                {'email': 'Данная почта уже занята'}
            )
        return attrs


class TokenSerializer(serializers.Serializer):

    username = serializers.CharField(required=True)
    confirmation_code = serializers.UUIDField(required=True)

    class Meta:
        fields = ('email', 'confirmation_code')

    def validate(self, data):
        confirmation_code = data.get('confirmation_code')
        user = get_object_or_404(User, username=data.get('username'))
        if not user.code_check(confirmation_code):
            raise ValidationError('Неправильный код подтверждения')
        refresh = RefreshToken.for_user(user)
        data['token'] = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return data
