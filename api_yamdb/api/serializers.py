from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Category, Genre, Title, User
#from .validators import ProhibitTheSameValues


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name','slug')
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }
    

class TitleSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(read_only=True, many=True)
    

    class Meta:
        fields = '__all__'
        model = Title


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'slug')
        model = Category

