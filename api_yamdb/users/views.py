import uuid
from http import HTTPStatus

from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .permissions import IsAdminOrSuper, IsAuth
from .serializers import GetTokenSerializer, UserSerializer
from .utils import Util


class UserViewSet(viewsets.ModelViewSet):
    """
    Эндпоинт users/
    Используется админами и суперпользователями.
    Исключение: users/me могут использовать авторизованные
    пользователи для просмотра и изменения своего профиля.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAdminOrSuper, )
    lookup_field = 'username'

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(
            queryset,
            username=self.kwargs[self.lookup_field]
        )
        return obj

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me',
        permission_classes=(IsAuth, ))
    def me(self, request, pk=None):
        data = request.data.copy()
        user = get_object_or_404(User, username=request.user.username)

        if request.method == 'GET':
            serializer = self.serializer_class(user)
            return Response(serializer.data)

        if not request.user.is_admin and not request.user.is_superuser:
            role = request.user.role
            data['role'] = role

        serializer = self.serializer_class(
            user,
            data=data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UserRegisterView(generics.GenericAPIView):
    """
    Регистрация нового пользователя.
    Принимаем username и email, высылаем на почту код.
    """
    serializer_class = UserSerializer

    def post(self, serializer):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user = User.objects.get(
            username=self.request.data['username'],
            email=self.request.data['email'],
        )

        user.confirmation_code = uuid.uuid4()
        user.save()

        email_body = f'Your confirmation code: {user.confirmation_code}'
        email_address = self.request.data['email']
        data = {
            'email_body': email_body,
            'subject': 'Email verification',
            'to': [email_address],
        }
        Util.send_email(data)

        return Response({
            "username": self.request.data['username'],
            "email": self.request.data['email'],
        })


class UserGetTokenView(generics.GenericAPIView):
    """
    Получение токена в ответ на username и confirmation_code
    """
    serializer_class = GetTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')
        confirmation_code = serializer.validated_data.get('confirmation_code')

        user = get_object_or_404(
            User,
            username=username,
        )
        if user.confirmation_code == confirmation_code:
            return Response(status=HTTPStatus.BAD_REQUEST)

        refresh = RefreshToken.for_user(user)
        return Response(str(refresh.access_token))
