from xml.etree.ElementInclude import include

from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import UserGetTokenView, UserRegisterView

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