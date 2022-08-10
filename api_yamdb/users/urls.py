from django.urls import path
from .views import UserRegisterView, UserGetTokenView

urlpatterns = [
    path('signup/', UserRegisterView.as_view(), name='signup'),
    path('token/', UserGetTokenView.as_view(), name='get_token')
]