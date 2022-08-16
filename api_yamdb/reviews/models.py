from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.constraints import UniqueConstraint

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.TextField(max_length=256)
    year = models.IntegerField()
    description = models.TextField(blank=True, null=True)

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='titles')

    genre = models.ManyToManyField(
        Genre, 
        through='GenreTitle',
        through_fields = ('title','genre')
    )

    rating = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} {self.genre}'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='review'
    )
    text = models.TextField()
    score = models.IntegerField(
        validators=[MinValueValidator(1, 'баллы должны быть в диапазоне от 1 до 10'),
                    MaxValueValidator(10, 'баллы должны быть в диапазоне от 1 до 10')],
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='review'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        constraints = (
            UniqueConstraint(fields=['author', 'title'],
                             name='unique_booking'),
        )


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True
    )
