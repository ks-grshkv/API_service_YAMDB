import datetime

from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        exclude = ('id',)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ('id',)


class SlugToModelGanreRelatedField(SlugRelatedField):
    def to_representation(self, instance):
        serializer = GenreSerializer(instance)
        return serializer.data


class SlugToModelCategoryRelatedField(SlugRelatedField):
    def to_representation(self, instance):
        serializer = CategorySerializer(instance)
        return serializer.data


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    genre = SlugToModelGanreRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True)

    category = SlugToModelCategoryRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug')

    class Meta:
        fields = '__all__'
        model = Title

    def create(self, validated_data):
        genres = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)

        for genre in genres:
            current_genre = get_object_or_404(Genre, name=genre)
            GenreTitle.objects.create(
                genre=current_genre, title=title)

        return title    
    
'''
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
        fields = '__all__'
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


    def create(self, validated_data):
        genres = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)

        for genre in genres:
            current_genre = get_object_or_404(Genre, name=genre)
            GenreTitle.objects.create(
                genre=current_genre, title=title)

        return title
'''

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
