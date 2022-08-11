from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Category, Genre, Title, Review, User
#from .validators import ProhibitTheSameValues


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name','slug')

class TitleSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(read_only=True, many=True)
    

    class Meta:
        fields = '__all__'
        model = Title


class CategorySerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Category

class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Review