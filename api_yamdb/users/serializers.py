from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from .models import User

print('ENTER SEIALISER')


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
