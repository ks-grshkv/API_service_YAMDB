from rest_framework import filters, permissions, viewsets
from .mixins import ListCreateDestroyViewset

from reviews.models import Category, Genre, Title, Review
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer, ReviewSerializer

from .permissions import IsAdminOrReadOnly


class CategoryViewSet(ListCreateDestroyViewset):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)

class GenreViewSet(ListCreateDestroyViewset):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)

class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer 
    permission_classes = (IsAdminOrReadOnly,)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminOrReadOnly,)
