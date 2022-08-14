from email.policy import default
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from .models import User, Roles

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
    role = serializers.CharField(
        default='user'
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

        def validate_role(self, role):
            print('ENTER ROLE VALIDTION')
            if role != Roles.admin or role != Roles.user or role != Roles.moderator:
                raise serializers.ValidationError('Invalid role')
            return role

        def validate_confirmation_code(self, confirmation_code):
            print('ENTER CONFIRMATION CODE VALIDATION')
            if confirmation_code is None:
                raise serializers.ValidationError('Empty confirmation_code')
            if not (confirmation_code is str):
                raise serializers.ValidationError('Confirmation_code should be str')
            if not (len(confirmation_code) == 5):
                raise serializers.ValidationError('Confirmation_code should be 5-digit long')
            return confirmation_code

        def validate(self, data):
            print('ENTER DATA VALIDTION')
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
