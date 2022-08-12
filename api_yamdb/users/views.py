# from .permissions import IsAuthorOrReadOnlyPermission
from random import randrange

from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .permissions import IsAdmin, IsAdminOrSelf
from .send_email import Util
from .serializers import UserGetTokenSerializer, UserSerializer

from http import HTTPStatus

from rest_framework.decorators import action


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,) 
    permission_classes = (IsAdminOrSelf, ) 

    def perform_create(self, serializer):

        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

    @action(detail=False, methods=['get', 'patch'], url_path='me')
    def me(self, request, pk=None):
        user = get_object_or_404(
            self.queryset, 
            username=self.request.user.username,
        )
        serializer = self.serializer_class(user)
        return Response(serializer.data)
        # data = {
        #     "username": self.request.user.username,
        #     "email": self.request.user.username,
        # }
        # serializer = get_object_or_404(
        #     UserSerializer,
        #     username=self.request.user.username,
        #     email=self.request.user.username,
        # )
        # serializer.is_valid(raise_exception=True)
        # return Response(serializer.data)

    @action(detail=True, methods=['get', 'patch'], url_path='')
    def username(self, request, pk=None):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

    def perform_update(self, serializer):
        pass


class UserRegisterView(generics.GenericAPIView):
    serializer_class = UserSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,) 

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



# class UserGetTokenView(generics.GenericAPIView):
#     serializer_class = UserSerializer
    
#     def post(self, request):
#         confirmation_code = self.request.data.get('confirmation_code')
#         username = self.request.data.get('username')
#         user = get_object_or_404(
#             User,
#             username=username,
#             confirmation_code=confirmation_code
#         )
#         refresh = RefreshToken.for_user(user)
#         return Response(str(refresh.access_token))


class UserGetTokenView(generics.GenericAPIView):
    serializer_class = UserSerializer
    
    def post(self, request):
        confirmation_code = self.request.data.get('confirmation_code')
        username = self.request.data.get('username')

        if (confirmation_code is None) or (username is None):
            return Response(status=HTTPStatus.BAD_REQUEST)
        try:
            user = get_object_or_404(
                User,
                username=username,
                confirmation_code=confirmation_code
            )
        except Exception as error:
            return Response(data=str(error), status=HTTPStatus.NOT_FOUND)
        try:
            user = get_object_or_404(
                User,
                username=username,
            )
            if confirmation_code != user.confirmation_code:
                return Response(status=HTTPStatus.BAD_REQUEST)
        except Exception as error:
            return Response(data=str(error), status=HTTPStatus.NOT_FOUND)
        refresh = RefreshToken.for_user(user)
        return Response(str(refresh.access_token))


# return Response(status=HTTPStatus.BAD_REQUEST)