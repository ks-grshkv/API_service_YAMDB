import datetime
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Category, Genre, GenreTitle, Review, Title, User, Comment


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')
      #  search_fields = ('slug',)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class SlugToModelGanreRelatedField(SlugRelatedField):
    def to_representation(self, instance):
        serializer = GenreSerializer(instance)
        return serializer.data


class SlugToModelCategoryRelatedField(SlugRelatedField):
    def to_representation(self, instance):
        serializer = CategorySerializer(instance)
        return serializer.data


class TitleSerializer(serializers.ModelSerializer):
    genre = SlugToModelGanreRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True)

    category = SlugToModelCategoryRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug')

    rating = serializers.FloatField(
        source='reviews__score__avg',
        read_only=True
    )

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category', 'rating',)
        model = Title

    def validate_year(self, value):
        year = datetime.date.today().year
        if year < value:
            raise serializers.ValidationError(
                'Год выпуска фильма не может быть больше текущего года!'
            )
        return value

    def validate_category(self, value):
        categories = Category.objects.all()
        categories_slug = {element.slug for element in categories}

        if value.slug not in categories_slug:
            raise serializers.ValidationError(
                'Вы ввели не существующую категорию!'
            )

        return value

    def validate_genre(self, value):
        genres = Genre.objects.all()
        categories_slug = {element.slug for element in genres}
        values_slug = {element.slug for element in genres}

        if len(values_slug & categories_slug) != len(categories_slug):
            raise serializers.ValidationError('Вы ввели не существующий жанр!')

        return value

    def create(self, validated_data):
        genres = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)

        for genre in genres:
            current_genre = get_object_or_404(Genre, name=genre)
            GenreTitle.objects.create(
                genre=current_genre, title=title)

        return title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('title',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'author', 'text', 'pub_date')
        model = Comment
        read_only_fields = ('review',)
