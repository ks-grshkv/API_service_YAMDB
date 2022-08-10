# from .permissions import IsAuthorOrReadOnlyPermission
from .serializers import UserSerializer, UserGetTokenSerializer
from .models import User

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from .send_email import Util
from rest_framework import viewsets, generics
# viewsets.ModelViewSet


class UserRegisterView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, serializer):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        email_body = 'test confrmation code: 0000FFFF0'
        email_address = self.request.data['email']
        data = {
            'email_body': email_body,
            'subject': 'Email verification',
            'to': [email_address],
        }
        Util.send_email(data)
        return Response(serializer.data)


class UserGetTokenView(APIView):
    serializer_class = UserGetTokenSerializer
    
    def post(self, request):
        serializer = UserGetTokenSerializer(data=self.request.data)
        confirmation_code = serializer.data.get('confirmation_code')
        username = serializer.data.get('username')
        user = User.objects.get(
            username=username,
            confirmation_code=confirmation_code
        )
        refresh = RefreshToken.for_user(user)
        result = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return Response(result)