from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import CategoryViewSet, GenreViewSet, TitleViewSet, ReviewViewSet

app_name = 'api'

router = SimpleRouter()

router.register('categories', CategoryViewSet)
router.register('titles', TitleViewSet)
router.register('genres', GenreViewSet)
router.register('titles/(?P<title_id>\\d+)/reviews', ReviewViewSet, basename='reviews')
# 'titles/(?P<title_id>\\d+)/reviews/(?P<review_id>\\d+)/comments'
urlpatterns = [
    path('v1/', include(router.urls)),
] 