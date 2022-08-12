# from .permissions import IsAuthorOrReadOnlyPermission
from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from random import randrange
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .permissions import IsAdmin
from .send_email import Util
from .serializers import UserGetTokenSerializer, UserSerializer

viewsets.ModelViewSet
from http import HTTPStatus


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,) 
    permission_classes = (IsAdmin,) 

    def perform_create(self, serializer):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

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


class UserGetTokenView(generics.GenericAPIView):
    serializer_class = UserSerializer
    
    def post(self, request):
        confirmation_code = self.request.data.get('confirmation_code')
        username = self.request.data.get('username')
        user = get_object_or_404(
            User,
            username=username,
            confirmation_code=confirmation_code
        )
        refresh = RefreshToken.for_user(user)
        return Response(str(refresh.access_token))