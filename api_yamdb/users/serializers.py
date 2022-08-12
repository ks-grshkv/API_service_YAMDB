from rest_framework import serializers

from .models import User
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=100,
        validators=[UniqueValidator(queryset=User.objects.all())],
        required=True
    )
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        required=True
    )

    class Meta:
        fields = ('username', 'bio', 'email', 'first_name', 'last_name', 'role')
        model = User

        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email']
            )
        ]

        def validate(self, data):
            print('VALIDATINGVALIDATINGVALIDATINGVALIDATING')
            user = self.context['request'].user
            if user.username is None:
                raise serializers.ValidationError('Empty username')
            if user.email is None:
                raise serializers.ValidationError('Empty email')
            if user.username == 'me':
                raise serializers.ValidationError('Invalid username')
            # if not validate_email(email, check_mx=True, verify=True):
            #     raise serializers.ValidationError("Invalid email")
            return data


class UserGetTokenSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = User
