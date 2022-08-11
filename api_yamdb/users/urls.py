from xml.etree.ElementInclude import include
from django.urls import path, include

from .views import UserGetTokenView, UserRegisterView
from rest_framework.routers import SimpleRouter

# app_name = 'users'

# router = SimpleRouter()

# router.register(
#     'users',
#     UserAPIView,
#     basename='users'
# )


urlpatterns = [
    path('signup/', UserRegisterView.as_view(), name='signup'),
    path('token/', UserGetTokenView.as_view(), name='get_token'),
    # path('users/', include(router.urls)),

]