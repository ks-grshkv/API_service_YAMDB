# from .permissions import IsAuthorOrReadOnlyPermission
from http import HTTPStatus
from random import randrange

from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Roles, User
from .permissions import IsAdmin, IsAdminOrAuth, IsAdminOrSelf
from .send_email import Util
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAdminOrSelf, )
    lookup_field = 'pk'

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(
            queryset,
            username=self.kwargs[self.lookup_field]
        )
        return obj

    def perform_update(self, serializer):
        user = get_object_or_404(
            self.queryset,
            username=self.kwargs[self.lookup_field]
        )
        serializer = self.serializer_class(
            user,
            data=self.request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
        if (user.role != Roles.admin) and (user.role != Roles.user) and (user.role != Roles.moderator):
            return Response(HTTPStatus.BAD_REQUEST)
        else:
            return Response(serializer.data)

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me',
        permission_classes=(IsAdminOrAuth, ))
    def me(self, request, pk=None):
        user = get_object_or_404(
            User,
            username=self.request.user.username,
        )

        if request.method == 'GET':
            serializer = self.serializer_class(user)
            return Response(serializer.data)
        else:
            data = {"role": request.user.role}
            serializer = self.serializer_class(
                user,
                data=request.data,
                partial=True
            )
            if serializer.is_valid():
                serializer.save()
            if (
                request.user.role != Roles.admin
            ) and not request.user.is_superuser:
                serializer = self.serializer_class(
                    user,
                    data=data,
                    partial=True
                )
            if serializer.is_valid():
                serializer.save()
        return Response(serializer.data)


class UserRegisterView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, serializer):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        if self.request.data['username'] == 'me':
            return Response(status=HTTPStatus.BAD_REQUEST)
        serializer.save()
        user = User.objects.get(
            username=self.request.data['username'],
            email=self.request.data['email'],
        )

        user.confirmation_code = randrange(10000, 100000)
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
    serializer_class = UserSerializer
    
    def post(self, request):
        confirmation_code = self.request.data.get('confirmation_code')
        username = self.request.data.get('username')

        if (confirmation_code is None) or (username is None):
            return Response(status=HTTPStatus.BAD_REQUEST)
        if (not User.objects.filter(
            username=username,
            confirmation_code=confirmation_code
        ).exists()) and User.objects.filter(username=username).exists():
            return Response(status=HTTPStatus.BAD_REQUEST)
        try:
            user = get_object_or_404(
                User,
                username=username,
                confirmation_code=confirmation_code
            )
        except Exception as error:
            return Response(data=str(error), status=HTTPStatus.NOT_FOUND)
        refresh = RefreshToken.for_user(user)
        return Response(str(refresh.access_token))

