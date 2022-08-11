from rest_framework import serializers

from .models import User
from rest_framework.validators import UniqueTogetherValidator


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = User
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email']
            )
        ]


class UserGetTokenSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = User
