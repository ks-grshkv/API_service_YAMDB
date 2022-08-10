from rest_framework.routers import SimpleRouter
from django.urls import include, path

from .views import CategoryViewSet, GenreViewSet, TitleViewSet

app_name = 'api'

router = SimpleRouter()

router.register('categories', CategoryViewSet)
router.register('titles', TitleViewSet)
router.register('genres', GenreViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 