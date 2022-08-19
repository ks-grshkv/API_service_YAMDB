from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet

router = DefaultRouter()

router.register(
    'users',
    UserViewSet,
    basename='users'
)

urlpatterns = [
    path('api/', include('api.urls', namespace='api')),
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('users.urls')),
    path('api/v1/', include(router.urls)),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]
