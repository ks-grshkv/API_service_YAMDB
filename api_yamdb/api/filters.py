from turtle import title
from django_filters import rest_framework
import django_filters

from reviews.models import Title


class TitleFilter(rest_framework.FilterSet):
    genre = rest_framework.CharFilter(field_name='genre__slug')
    category = rest_framework.CharFilter(field_name='category__slug')
    name = rest_framework.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Title
        fields = ['name', 'year', 'genre', 'category']