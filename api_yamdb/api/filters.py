from turtle import title
from django_filters import rest_framework
import django_filters

from reviews.models import Title

class CharFilterInclude(rest_framework.CharFilter):
     def filter(self, qs, value):
        strs = value.split(',')
        if len(strs) != 2:
            raise Exception

        return qs.filter(
            food_components__in = Component.objects.filter(
                name=strs[0],
                value=float(strs[1])
            )
        )

class TitleFilter(rest_framework.FilterSet):
    genre = rest_framework.CharFilter(field_name='genre__slug')
    category = rest_framework.CharFilter(field_name='category__slug')
 #   name = CharFilterInclude(field_name='name')
 #   name = django_filters.MethodFilter(name='name', action='icontains')

    class Meta:
        model = Title
        fields = ['name', 'year', 'genre', 'year']

    def icontains(self, queryset, value):
        #return queryset.filter(reduce(lambda x, y: x | y, [Q(title__icontains=word) for word in query_words]))
        return queryset.filter(Title.objects.filter(name__contains=value))
