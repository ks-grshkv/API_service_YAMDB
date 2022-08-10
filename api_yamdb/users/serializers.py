from .models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = User


class UserGetTokenSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = User
