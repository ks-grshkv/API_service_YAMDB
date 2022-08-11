# from .permissions import IsAuthorOrReadOnlyPermission
from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .permissions import IsAdmin
from .send_email import Util
from .serializers import UserGetTokenSerializer, UserSerializer

viewsets.ModelViewSet


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,) 
    permission_classes = (IsAdmin,) 

    def perform_create(self, serializer):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()


class UserRegisterView(generics.GenericAPIView):
    serializer_class = UserSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,) 

    def post(self, serializer):
        confirmation_code = User.get_confirmation_code(self)
        data = {
            "username": self.request.data['username'],
            "email": self.request.data['email'],
            "confirmation_code": confirmation_code
        }
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        email_body = f'Your confirmation code: {confirmation_code}'
        email_address = self.request.data['email']
        data = {
            'email_body': email_body,
            'subject': 'Email verification',
            'to': [email_address],
        }
        Util.send_email(data)
        return Response(serializer.data)


class UserGetTokenView(generics.GenericAPIView):
    serializer_class = UserSerializer
    
    def post(self, request):
        confirmation_code = self.request.data.get('confirmation_code')
        username = self.request.data.get('username')
        user = User.objects.get(
            username=username,
            confirmation_code=confirmation_code
        )
        refresh = RefreshToken.for_user(user)
        return Response(str(refresh.access_token))