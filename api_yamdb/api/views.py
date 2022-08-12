from rest_framework import filters, permissions, viewsets
from reviews.models import Category, Genre, Title

from .mixins import ListCreateDestroyViewset
from .permissions import IsAdminOrReadOnly
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer


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
