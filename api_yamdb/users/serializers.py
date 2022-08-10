from .models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer):
    username = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        validators = [
            UniqueValidator(queryset=User.objects.all()),
        ]
    )

    class Meta:
        fields = '__all__'
        model = User
        # validators = [
        #     UniqueValidator(queryset=User.objects.all()),
        # ]


class UserGetTokenSerializer(serializers.ModelSerializer):
    username = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        fields = '__all__'
        model = User
        validators = [
            UniqueValidator(queryset=User.objects.all()),
        ]