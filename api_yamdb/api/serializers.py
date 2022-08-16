import datetime

from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


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

    rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
            'rating',)
        model = Title

    def get_rating(self, obj):
        rating = obj.review.aggregate(Avg('score')).get('score__avg')
        return rating

    def validate_year(self, value):
        year = datetime.date.today().year
        if year < value:
            raise serializers.ValidationError(
                'Год выпуска фильма не может быть больше текущего года!'
            )
        return value

    def validate_category(self, value):
        print('VALIDATING DATA', self.context['view'])
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
    title = serializers.SlugRelatedField(
        read_only=True, slug_field='name'
    )

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('title',)

    def validate(self, data):
        author = self.context['request'].user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(
            Title,
            pk=title_id,
        )
        queryset_len = Review.objects.filter(
            author=author,
            title=title
        ).count()
        if queryset_len > 0 and self.context['request'].method == 'POST':
            print('invalid!!!!!!', Review.objects.filter(
                author=author,
                title=title
            ))
            raise serializers.ValidationError('Нельзя оставить 2 ревью')
        else:
            return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'author', 'text', 'pub_date')
        model = Comment
        read_only_fields = ('review',)
