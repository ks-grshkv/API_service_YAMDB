from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from .models import User


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=100,
        validators=[UniqueValidator(queryset=User.objects.all())],
        required=True,
    )
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        required=True
    )

    class Meta:
        fields = (
            'username',
            'bio',
            'email',
            'first_name',
            'last_name',
            'role'
        )
        model = User

        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email']
            )
        ]

    def validate_username(self, value):

        """
        Проверяем, что нельзя сделать юзернейм 'me'
        """
        if value == 'me':
            raise serializers.ValidationError('Задайте другой юзернейм')
        if value is None:
            raise serializers.ValidationError('Задайте не пустой юзернейм')
        return value

    def create(self, validated_data):
        return User.objects.create(**validated_data)


class GetTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=100,
        validators=[UniqueValidator(queryset=User.objects.all())],
        required=True,
    )

    class Meta:
        fields = (
            'username',
            'confirmation_code'
        )
        model = User

    def validate(self, data):
        """
        Проверяем, что нельзя код подтвердения и юзернейм не пустые
        """
        if (
            (data.get('username') is None)
            or (data.get('confirmation_code') is None)
        ):
            raise serializers.ValidationError('Задайте не пустой юзернейм')
        return data
